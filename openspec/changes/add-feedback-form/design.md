## Context

Voir proposal.md - Why. Deux apps existantes offrent des précédents directement réutilisables :
- `contacts` (forms.py / services.py / emails.py / views.py / urls.py) pour le pattern d'envoi d'email avec `render_to_string` + `logging.exception` en cas d'échec SMTP (`contacts/emails.py`).
- `moderation` (`moderation/views.py`, `moderation/templates/moderation/report.html`) pour le pattern d'une page de formulaire dédiée, `login_required` + `require_http_methods`/`require_POST`.

Aucun des deux n'est le bon capability-fit sémantique pour un message libre destiné au superadmin (voir proposal.md - Capabilities).

## Goals / Non-Goals

**Goals:**
- Un parcours minimal : lien dans le header → page → formulaire à un champ → email.
- Réutiliser les patterns déjà en place (structure d'app, gestion d'email) plutôt qu'en inventer de nouveaux.

**Non-Goals:**
- Pas de persistance ni d'historique des messages envoyés (voir proposal.md).
- Pas de catégorisation du message (question/idée/commentaire) côté système : c'est une indication donnée à l'utilisateur via le placeholder, pas une donnée structurée.
- Pas de rate-limiting ni de protection anti-abus.

## Decisions

**Nouvelle app Django `feedback`, sans `models.py`.**
Suit le découpage par capability du projet (une app = une responsabilité). Fichiers : `forms.py`, `views.py`, `emails.py`, `urls.py`, plus `templates/feedback/send.html`. Alternative écartée : ajouter une vue dans `contacts` ou `moderation` — rejetée car sémantiquement hors périmètre de ces apps (lien avec un item/une demande, ou signalement d'abus).

**Destinataire via variable d'environnement `FEEDBACK_RECIPIENT_EMAIL`.**
Ajoutée dans `config/settings.py` à côté de `SITE_URL`/`DEFAULT_FROM_EMAIL`, lue via `os.environ.get(...)`. Alternative écartée : interroger `User.objects.filter(is_superuser=True)` — plus "vivant" mais introduit une ambiguïté (plusieurs superusers) pour aucun bénéfice actuel ; l'app est en phase alpha avec un superadmin unique et connu.

**Reply-To plutôt qu'email en texte dans le corps uniquement.**
`django.core.mail.EmailMessage(subject, body, from_email, [recipient], reply_to=[user.email])` au lieu de `send_mail` (qui ne supporte pas `reply_to`). Le corps inclut aussi l'adresse en clair, en secours si le client mail du superadmin ignore l'en-tête `Reply-To`.

**Pas de persistance (fire-and-forget).**
Décision explicite de l'utilisateur. Conséquence acceptée : si l'envoi SMTP échoue, `emails.py` logue l'exception (même pattern que `contacts/emails.py`) mais la vue affiche quand même un message de succès à l'utilisateur, qui croira son message transmis alors qu'il est perdu. Pas de filet de sécurité côté admin (pas de trace en base, pas de visibilité dans l'admin Django). Documenté ici pour que ce compromis reste traçable si on veut le revisiter plus tard.

**Formulaire à un seul champ texte libre, pas de `ChoiceField`.**
Le placeholder du `Textarea` guide l'utilisateur ("Une question, une idée d'amélioration, un commentaire...") sans imposer de structure. Validation : champ requis, non vide.

**Point d'entrée dans le dropdown "Mon compte" (`templates/base.html`).**
Cohérent avec les autres liens réservés aux connectés ("Mes objets", "Mon profil", etc.). Mène à une page dédiée (`GET` affiche le formulaire, `POST` l'envoie), sur le même modèle que `moderation/report.html`.

## Risks / Trade-offs

- [Perte silencieuse du message si le SMTP échoue] → Acceptée pour la phase alpha (base d'utilisateurs restreinte et de confiance) ; à revisiter si le volume ou la criticité augmentent (ajout possible d'un modèle de secours sans changer l'UX).
- [Pas de protection anti-abus] → Acceptée : fonctionnalité réservée aux utilisateurs authentifiés, base alpha restreinte (voir proposal.md - Impact).
