## 1. App scaffolding

- [x] 1.1 Créer l'app `feedback` (`manage.py startapp feedback`) avec `apps.py`, `urls.py`, `forms.py`, `views.py`, `emails.py` (pas de `models.py`)
- [x] 1.2 Ajouter `feedback` à `INSTALLED_APPS` dans `config/settings.py`
- [x] 1.3 Inclure `feedback.urls` dans `config/urls.py`

## 2. Configuration

- [x] 2.1 Ajouter `FEEDBACK_RECIPIENT_EMAIL = os.environ.get("FEEDBACK_RECIPIENT_EMAIL") or ...` dans `config/settings.py`, à côté de `SITE_URL`/`DEFAULT_FROM_EMAIL`
- [x] 2.2 Documenter la variable d'environnement (README ou équivalent si les autres variables y sont déjà listées)

## 3. Formulaire et vue

- [x] 3.1 `feedback/forms.py` : `FeedbackForm` avec un `CharField`/`Textarea` requis, placeholder "Une question, une idée d'amélioration, un commentaire..."
- [x] 3.2 `feedback/views.py` : vue `send` (`GET` affiche le formulaire, `POST` le valide et envoie), décorée `@login_required`
- [x] 3.3 `feedback/urls.py` : route nommée (ex. `feedback:send`)
- [x] 3.4 Template `feedback/templates/feedback/send.html` (extends `base.html`, même structure que `moderation/templates/moderation/report.html` : titre, formulaire, bouton d'envoi, lien d'annulation)
- [x] 3.5 Message de confirmation (`django.contrib.messages`) après envoi réussi, puis redirection

## 4. Email

- [x] 4.1 `feedback/emails.py` : fonction d'envoi utilisant `django.core.mail.EmailMessage` avec `to=[settings.FEEDBACK_RECIPIENT_EMAIL]`, `reply_to=[user.email]`, corps contenant le message et l'email de l'utilisateur
- [x] 4.2 Gestion de l'échec d'envoi : logguer l'exception sans faire échouer la requête (même pattern que `contacts/emails.py`)

## 5. Intégration UI

- [x] 5.1 Ajouter un lien vers `feedback:send` dans le dropdown "Mon compte" de `templates/base.html`

## 6. Tests

- [x] 6.1 Test : un visiteur non connecté est redirigé vers la connexion en accédant au formulaire
- [x] 6.2 Test : un membre connecté soumettant un message valide reçoit une confirmation et un email est envoyé avec le bon destinataire et le bon `Reply-To`
- [x] 6.3 Test : soumission avec message vide refusée, avec message d'erreur
