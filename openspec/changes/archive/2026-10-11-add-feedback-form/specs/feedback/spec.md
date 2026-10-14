## Purpose

Donne à tout membre connecté un moyen simple d'envoyer une question, une idée d'amélioration ou un commentaire au superadmin, transmis directement par email.

## ADDED Requirements

### Requirement: Envoi d'un message au superadmin

Le système MUST permettre à un membre connecté d'envoyer un message libre (texte, non catégorisé) destiné au superadmin. Un visiteur non connecté MUST ne pas pouvoir accéder à ce formulaire.

#### Scenario: Envoi réussi

- **WHEN** un membre connecté soumet le formulaire avec un message non vide
- **THEN** un email est envoyé au superadmin contenant le message et l'adresse email du membre, et le membre voit une confirmation d'envoi

#### Scenario: Message vide

- **WHEN** un membre connecté soumet le formulaire sans message
- **THEN** le système refuse l'envoi et affiche une erreur

#### Scenario: Visiteur non connecté

- **WHEN** un visiteur non connecté tente d'accéder au formulaire de contact
- **THEN** le système le redirige vers la connexion

### Requirement: Email exploitable pour répondre au membre

Le système MUST envoyer l'email de notification de façon à ce que le superadmin puisse répondre directement au membre à l'origine du message (répondre à l'email revient à écrire à l'adresse du membre).

#### Scenario: Réponse directe

- **WHEN** le superadmin répond à l'email de notification reçu
- **THEN** la réponse est adressée au membre qui a envoyé le message
