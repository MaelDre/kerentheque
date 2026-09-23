## Context

Le dépôt ne contient encore aucun code : ce change crée le projet. Voir `proposal.md` pour la motivation et les specs (`user-accounts`, `item-management`, `catalog`, `contact-requests`, `moderation`) pour le comportement attendu.

Contraintes qui orientent la conception :
- application destinée à de vrais utilisateurs, mais petit projet maintenu par une seule personne : chaque dépendance et chaque couche doit se justifier ;
- web app responsive, sans application mobile ;
- données personnelles (email, téléphone) transmises entre utilisateurs, donc exigences RGPD ;
- hébergement non encore choisi (Railway envisagé) : le code ne doit dépendre d'aucune plateforme.

## Goals / Non-Goals

**Goals:**
- Un seul projet Django monolithique, rendu côté serveur, sans étape de build front.
- Règles métier (annulations, transitions de statut, suppression de compte) centralisées dans une couche de services, appelée aussi bien par les vues que par l'admin.
- Configuration entièrement par variables d'environnement, pour déployer n'importe où.

**Non-Goals:**
- Pas d'API (REST ou autre) ni de JavaScript applicatif.
- Pas d'envoi d'emails asynchrone (file de tâches) pour le MVP.
- Pas de configuration de déploiement (Dockerfile, fichiers Railway) : traité dans un change ultérieur.

## Decisions

### Stack
- **Python 3.12+, Django 5.2 (LTS)**, SQLite, gestion du projet avec **uv** (`pyproject.toml` + lockfile).
  *Alternative :* pip + `requirements.txt`. uv donne un lockfile reproductible sans effort supplémentaire.
- **Pico CSS** copié dans `static/` (pas de CDN), complété par une petite feuille de style propre au projet.
- **WhiteNoise** pour servir les fichiers statiques depuis Django : une seule ligne de middleware, et aucun serveur web séparé n'est nécessaire au déploiement.
- Langue et fuseau : `fr-fr`, `Europe/Paris`. Interface uniquement en français, sans mécanisme de traduction.

### Découpage en apps Django

```
config/        settings, urls racine, wsgi
accounts/      User, Neighborhood, connexion, profil, suppression de compte, pages légales
items/         Category, Item, catalogue, fiche objet, « Mes objets »
contacts/      ContactRequest, envoi, décisions, « Mes demandes », « Demandes reçues », emails
moderation/    Report, actions d'admin (suspension, retrait d'objet)
templates/     base.html + templates par app
```

Le nom `contacts` évite le conflit avec la bibliothèque `requests`.

### Modèle de données

```
User (AbstractBaseUser)                 Item
  email        unique                     owner        FK User
  pseudo       unique (Lower), null        name, description
  neighborhood FK Neighborhood PROTECT     category     FK Category PROTECT
  phone        blank                       created_at
  share_email, share_phone  bool           deleted_at   null   ← suppression logique
  terms_accepted_at  null                  search_text        ← nom+description normalisés
  is_active (False = suspendu/supprimé)
  deleted_at   null                     ContactRequest
  is_staff                                 item         FK Item
                                           requester    FK User
Category / Neighborhood                    status       pending|accepted|refused|cancelled
  name, position, is_active                message
                                           item_name           ← copie du nom de l'objet
Report                                     requester_email, requester_phone ← figés à l'envoi
  author FK User                           owner_email, owner_phone         ← figés à l'acceptation
  item FK Item null / user FK User null    created_at, decided_at
  reason, created_at, handled_at null      UniqueConstraint(item, requester)
```

- **Profil complet** = `pseudo`, `neighborhood` et `terms_accepted_at` renseignés. Un middleware redirige vers le formulaire de profil tant que ce n'est pas le cas.
- **Coordonnées figées** : les colonnes copiées dans `ContactRequest` implémentent la spec « coordonnées figées ». Elles ne contiennent que les canaux partagés au moment de la transmission, ce qui garantit qu'un canal non consenti n'est jamais exposé.
- **`item_name` copié** : garde le nom lisible dans l'historique même après suppression ou modification de l'objet.
- **Suppression logique des objets** (`deleted_at`) plutôt qu'un effacement réel : conserve le lien avec les demandes et les signalements. Un manager `Item.available` filtre les objets non supprimés dont le propriétaire est actif.
- **Suppression de compte = anonymisation** : l'email est remplacé par une valeur unique non routable (`deleted-<id>@invalid`), le pseudo et le téléphone sont vidés, les coordonnées figées dans les demandes le concernant sont effacées, `is_active=False` et `deleted_at` sont renseignés. L'email réel redevient libre pour une nouvelle inscription. Les templates affichent « Utilisateur supprimé » quand `deleted_at` est renseigné.
  *Alternative :* suppression réelle en cascade. Elle ferait disparaître les demandes de l'historique des autres utilisateurs, ce qui contredit la spec.
- Les `FK ... PROTECT` sur Category et Neighborhood empêchent la suppression d'une valeur utilisée (spec moderation) ; la désactivation passe par `is_active`.

### Connexion par lien magique : django-sesame
- `SESAME_MAX_AGE = 900` (15 min) et `SESAME_ONE_TIME = True` (le jeton est invalidé par la mise à jour de `last_login`).
- django-sesame génère un jeton pour un utilisateur existant. Lors d'une demande de lien pour un email inconnu, on crée donc un `User` sans profil. Il n'est visible nulle part tant que son profil n'est pas complété. Une commande de maintenance supprime ces comptes jamais connectés après 7 jours.
  *Alternative :* un jeton maison signé (`django.core.signing`) portant l'email, sans créer de compte à l'avance. Mais il faudrait réimplémenter l'usage unique ; sesame est éprouvé et tient en quelques lignes de configuration.
- Les comptes `is_active=False` (suspendus ou supprimés) sont refusés par sesame, ce qui implémente « un compte suspendu ne peut plus se connecter ».
- **Limitation d'envoi** : au plus une demande de lien par email et par minute, via le cache Django (mémoire locale), pour éviter qu'on utilise le formulaire pour inonder une boîte mail.

### Couche de services
Les règles qui touchent plusieurs modèles sont des fonctions dans un `services.py` par app, exécutées dans `transaction.atomic()` :
- `items.services.delete_item(item)` : renseigne `deleted_at` et annule les demandes en attente ;
- `contacts.services.send_request(...)`, `accept(...)`, `refuse(...)`, `cancel_pending_for_item(...)`, `cancel_pending_for_user(...)` ;
- `accounts.services.delete_account(user)` et `moderation.services.suspend_user(user)` / `reactivate_user(user)`.

Les vues et les actions d'admin appellent ces fonctions et ne modifient jamais les statuts directement. Dans l'admin, l'action groupée par défaut `delete_selected` est désactivée pour Item et User, et remplacée par des actions qui passent par les services.

**Transitions de statut sans conflit** : `accept` et `refuse` utilisent une mise à jour conditionnelle (`filter(pk=..., status="pending").update(...)`). Si aucune ligne n'est modifiée, c'est que la demande n'était plus en attente, et l'action est rejetée. Cela implémente « décision définitive » même en cas de double clic ou de course avec une annulation.

**Limite de 5 demandes en attente** : comptage dans la même transaction que la création. SQLite sérialise les écritures, ce qui suffit à ce volume. La contrainte d'unicité `(item, requester)` garantit l'absence de doublon au niveau de la base.

### Recherche
SQLite ne compare sans distinction de casse que les caractères ASCII : `icontains` ne ferait pas correspondre « echelle » et « Échelle ». Chaque objet stocke donc un champ `search_text` (nom et description en minuscules, sans accents), recalculé à l'enregistrement. La requête est normalisée de la même façon avant un `contains`.
*Alternative :* SQLite FTS5. C'est plus puissant, mais demande des tables virtuelles et des requêtes SQL brutes, ce qui est disproportionné pour quelques centaines d'objets.

### Emails
- Emails en texte brut, rendus depuis des templates Django (`contacts/emails/*.txt`).
- Envoi synchrone dans `transaction.on_commit()` : l'email ne part que si la transaction a réussi. Un échec d'envoi est journalisé et n'annule pas l'action.
- Backend configurable : console en développement, SMTP en production (`EMAIL_URL` ou variables `EMAIL_HOST`, etc.). Tous les grands services transactionnels proposent du SMTP, donc le choix du service n'affecte pas le code.
- `SITE_URL` (variable d'environnement) sert à construire les liens absolus dans les emails.

### Configuration
Variables d'environnement lues avec `os.environ` dans `settings.py`, sans bibliothèque supplémentaire : `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_PATH`, `SITE_URL`, `DEFAULT_FROM_EMAIL` et les paramètres SMTP. Un fichier `.env.example` les documente. Avec `DEBUG=False`, les réglages de sécurité sont activés : cookies `Secure`, HSTS, redirection HTTPS.

SQLite est configuré en mode WAL au démarrage, pour que les lectures ne soient pas bloquées par les écritures.

### Tests
Test runner de Django (`manage.py test`), sans dépendance supplémentaire. Les tests se concentrent sur les services (transitions, annulations, anonymisation, coordonnées figées) et sur les contrôles d'accès des vues. Chaque scénario des specs sert de base à un cas de test.

## Risks / Trade-offs

- [Envoi d'email synchrone : une lenteur du serveur SMTP ralentit la requête de l'utilisateur] → Acceptable au volume prévu. On garde un délai d'expiration SMTP court (10 s), et un passage à une file de tâches reste possible sans changer les services.
- [SQLite : un seul processus d'écriture] → Suffisant pour une zone restreinte. Le mode WAL améliore la concurrence en lecture. La migration vers PostgreSQL ne demande qu'un changement de `DATABASES`.
- [Perte du fichier SQLite si l'hébergeur n'a pas de disque persistant] → Chemin configurable via `DATABASE_PATH`. Le change de déploiement devra monter un volume et prévoir une sauvegarde.
- [Comptes créés à la demande de lien pour des emails jamais confirmés] → Invisibles tant que le profil est incomplet, et purgés après 7 jours par la commande de maintenance.
- [Emails de connexion classés en spam] → Dépend du service d'envoi (SPF, DKIM) : à traiter au déploiement. Le message après demande de lien invite à vérifier les spams.
- [Formulaires utilisables pour du spam de demandes] → Limite de 5 demandes en attente, unicité par objet, possibilité de suspension par l'admin.
- [Le propriétaire voit les coordonnées du demandeur même s'il refuse] → Comportement voulu et accepté explicitement par le demandeur à l'envoi. La politique de confidentialité le mentionne.

## Migration Plan

Premier déploiement : aucune donnée existante. Après le déploiement, on crée un super-utilisateur (`createsuperuser`) puis on saisit les quartiers et les catégories initiaux dans l'admin. Une migration de données peut proposer une liste de catégories par défaut, modifiable ensuite. Le plan de déploiement détaillé relève du change dédié.

## Open Questions

- Service d'envoi d'emails et hébergeur : choisis au déploiement, sans impact sur le code (SMTP et variables d'environnement).
- Contenu exact des mentions légales et de la politique de confidentialité (éditeur, hébergeur, contact) : à rédiger avant la mise en ligne. Les pages sont prévues dans le MVP, avec un texte provisoire.
- Format du téléphone : validation souple pour le MVP (chiffres, espaces, `+`, entre 10 et 15 chiffres). À durcir si des numéros invalides apparaissent.
- Liste initiale des catégories et des quartiers : à fournir par le porteur du projet.
