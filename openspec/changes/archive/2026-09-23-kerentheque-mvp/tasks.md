## 1. Initialisation du projet

- [x] 1.1 Initialiser le projet avec uv (`pyproject.toml`, Python 3.12+) et ajouter Django 5.2, django-sesame et WhiteNoise
- [x] 1.2 Créer le projet Django `config/` et les apps `accounts`, `items`, `contacts`, `moderation`
- [x] 1.3 Écrire `settings.py` piloté par variables d'environnement (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_PATH`, `SITE_URL`, `DEFAULT_FROM_EMAIL`, SMTP) avec les réglages de sécurité si `DEBUG=False`, et fournir `.env.example`
- [x] 1.4 Configurer la langue `fr-fr`, le fuseau `Europe/Paris`, le backend email console en développement, SQLite en mode WAL, WhiteNoise pour les statiques
- [x] 1.5 Ajouter Pico CSS dans `static/`, créer `base.html` (navigation responsive, messages, liens vers les pages légales) et une feuille de style projet minimale
- [x] 1.6 Ajouter un `.gitignore` (base SQLite, `.env`, environnement virtuel) et un README décrivant l'installation et le lancement en local

## 2. Référentiels et modèle utilisateur

- [x] 2.1 Créer le modèle `Neighborhood` (nom, position, `is_active`) et son admin (ordre, désactivation)
- [x] 2.2 Créer le modèle `User` personnalisé (email unique comme identifiant, pseudo unique insensible à la casse, quartier en `PROTECT`, téléphone, `share_email`, `share_phone`, `terms_accepted_at`, `deleted_at`) et le déclarer dans `AUTH_USER_MODEL` avant la première migration
- [x] 2.3 Créer le modèle `Category` (nom, position, `is_active`) et son admin
- [x] 2.4 Ajouter une migration de données avec une liste de catégories par défaut modifiable dans l'admin
- [x] 2.5 Tests : unicité du pseudo sans distinction de casse, suppression impossible d'une catégorie ou d'un quartier utilisé

## 3. Connexion et profil

- [x] 3.1 Configurer django-sesame (expiration 15 min, usage unique) et le backend d'authentification
- [x] 3.2 Page de demande de lien : saisie de l'email, création d'un compte sans profil si l'email est inconnu, envoi du lien, message identique que le compte existe ou non, limite d'une demande par email et par minute
- [x] 3.3 Vue de connexion par lien, avec une page d'erreur pour un lien expiré ou déjà utilisé qui propose un nouveau lien
- [x] 3.4 Formulaire de profil (pseudo, quartier actif, téléphone, réglages de partage, acceptation des conditions) avec les validations : au moins un canal, téléphone requis pour le partager, format du téléphone
- [x] 3.5 Middleware qui redirige vers le formulaire de profil tant que celui-ci est incomplet (sauf pages publiques, légales et de déconnexion)
- [x] 3.6 Page de modification du profil (email affiché en lecture seule) et déconnexion
- [x] 3.7 Pages mentions légales et politique de confidentialité avec un texte provisoire
- [x] 3.8 Commande de maintenance qui purge les comptes jamais connectés depuis plus de 7 jours
- [x] 3.9 Tests : lien valide, expiré ou réutilisé ; compte suspendu refusé ; redirection vers le profil incomplet ; règles de partage

## 4. Objets

- [x] 4.1 Créer le modèle `Item` (propriétaire, nom, catégorie en `PROTECT`, description, `created_at`, `deleted_at`, `search_text` normalisé à l'enregistrement) et le manager `available`
- [x] 4.2 Écrire la fonction de normalisation du texte (minuscules, sans accents), partagée entre l'indexation et la recherche
- [x] 4.3 Formulaires d'ajout et de modification (catégories actives uniquement, limites de longueur), réservés au propriétaire
- [x] 4.4 Page « Mes objets »
- [x] 4.5 Service `delete_item` (suppression logique et annulation des demandes en attente) et vue de suppression avec confirmation
- [x] 4.6 Tests : droits du propriétaire, validations, suppression logique

## 5. Catalogue

- [x] 5.1 Vue catalogue publique : objets disponibles, les plus récents en premier, pagination par 20
- [x] 5.2 Recherche texte sur `search_text` et filtres par catégorie et par quartier, combinables et conservés dans l'URL
- [x] 5.3 Fiche objet : informations publiques, état selon le visiteur (invitation à se connecter, bouton de demande, statut de la demande existante, lien de modification pour le propriétaire), page « objet introuvable » si l'objet est supprimé ou appartient à un compte suspendu
- [x] 5.4 Tests : visibilité (objet supprimé, propriétaire suspendu), recherche avec accents, combinaison de filtres, aucune donnée privée dans les pages publiques

## 6. Demandes de contact

- [x] 6.1 Créer le modèle `ContactRequest` (statuts, message, `item_name`, coordonnées figées du demandeur et du propriétaire, dates, contrainte d'unicité `(item, requester)`)
- [x] 6.2 Service `send_request` : contrôles (pas son propre objet, objet disponible, pas de doublon, au plus 5 demandes en attente), copie des coordonnées partagées du demandeur, email au propriétaire après validation de la transaction
- [x] 6.3 Formulaire d'envoi sur la fiche objet : message facultatif, affichage des coordonnées qui seront transmises, case de consentement obligatoire
- [x] 6.4 Services `accept` et `refuse` avec mise à jour conditionnelle sur le statut « en attente » ; `accept` copie les coordonnées partagées du propriétaire et envoie l'email au demandeur, `refuse` n'envoie rien
- [x] 6.5 Services `cancel_pending_for_item` et `cancel_pending_for_user` (sans notification)
- [x] 6.6 Templates d'email en texte brut : nouvelle demande et demande acceptée, avec liens absolus construits sur `SITE_URL`
- [x] 6.7 Page « Mes demandes » (demandes envoyées, statut, coordonnées du propriétaire si acceptée, « Utilisateur supprimé » si besoin)
- [x] 6.8 Page « Demandes reçues » (en attente en premier, coordonnées du demandeur, boutons accepter et refuser)
- [x] 6.9 Tests : cycle complet, décision définitive, décision par un tiers refusée, limite de 5, doublon après refus, coordonnées figées après changement de réglages, emails envoyés ou non selon le cas

## 7. Suppression de compte

- [x] 7.1 Service `delete_account` : anonymisation (email non routable, pseudo et téléphone vidés, `is_active=False`, `deleted_at`), suppression logique des objets, annulation des demandes en attente envoyées et reçues, effacement des coordonnées figées concernant l'utilisateur
- [x] 7.2 Page de suppression de compte avec confirmation, puis déconnexion
- [x] 7.3 Tests : données effacées, historique affiché comme « Utilisateur supprimé », nouvelle inscription possible avec le même email

## 8. Modération

- [x] 8.1 Créer le modèle `Report` (auteur, objet ou utilisateur ciblé, motif, dates) et le formulaire de signalement depuis la fiche objet (pas pour soi-même ni ses propres objets)
- [x] 8.2 Admin des signalements : liste des signalements non traités, liens vers la cible, action « marquer comme traité »
- [x] 8.3 Services `suspend_user` et `reactivate_user`, exposés comme actions d'admin sur les utilisateurs
- [x] 8.4 Admin des objets : action de retrait passant par `delete_item`, et désactivation de `delete_selected` pour Item et User
- [x] 8.5 Tests : suspension (connexion refusée, objets masqués, demandes annulées), réactivation, retrait d'un objet, admin inaccessible aux membres

## 9. Finitions

- [x] 9.1 Vérifier chaque page sur un écran de 360 px (sans défilement horizontal) et sur ordinateur
- [x] 9.2 Pages d'erreur 404 et 500 dans le style du site
- [x] 9.3 Relire les textes de l'interface et des emails (ton, clarté du consentement, statuts)
- [x] 9.4 Lancer toute la suite de tests et `manage.py check --deploy` avec une configuration de production
