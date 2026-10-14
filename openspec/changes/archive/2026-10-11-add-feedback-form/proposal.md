## Why

Les utilisateurs n'ont aucun moyen, dans l'application, de signaler une question, de suggérer une amélioration ou de laisser un commentaire au superadmin. Le seul canal existant (`moderation`) est réservé au signalement d'objets ou d'utilisateurs problématiques, pas à la discussion générale avec l'équipe. En phase alpha, ce retour direct est précieux et doit être simple à envoyer.

## What Changes

- Ajout d'un lien « Nous contacter » (ou équivalent) dans le dropdown « Mon compte » du header, visible uniquement pour les utilisateurs authentifiés.
- Ajout d'une page dédiée avec un formulaire à un seul champ libre (texte), avec un placeholder invitant à poser une question, suggérer une idée ou laisser un commentaire.
- À la soumission, envoi d'un email au superadmin contenant le message et l'email de l'utilisateur en `Reply-To`, pour permettre une réponse directe.
- Aucune persistance en base : le message n'est pas stocké, seul l'envoi d'email fait foi (compromis assumé pour la simplicité en phase alpha).
- Nouvelle variable d'environnement `FEEDBACK_RECIPIENT_EMAIL` pour désigner l'adresse de réception, suivant le même pattern que `SITE_URL`/`DEFAULT_FROM_EMAIL`.

## Capabilities

### New Capabilities
- `feedback`: permet à un utilisateur authentifié d'envoyer un message libre (question, idée, commentaire) qui est transmis par email au superadmin, avec son adresse en `Reply-To`.

### Modified Capabilities
(aucune)

## Impact

- Nouvelle app Django `feedback` (forms.py, views.py, emails.py, urls.py — pas de models.py).
- `config/settings.py` : nouvelle variable `FEEDBACK_RECIPIENT_EMAIL`, nouvelle entrée dans `INSTALLED_APPS`.
- `config/urls.py` : inclusion des URLs de l'app `feedback`.
- `templates/base.html` : ajout d'un lien dans le dropdown « Mon compte ».
- Dépendance à la configuration email existante (SMTP/console backend déjà en place, aucun changement requis côté infra).
