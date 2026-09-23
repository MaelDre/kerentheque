# contact-requests Specification

## Purpose

Met en relation un membre intéressé par un objet et son propriétaire : le demandeur transmet ses coordonnées avec sa demande, et le propriétaire décide s'il transmet les siennes en retour. Le prêt se déroule ensuite hors de l'application.

## Requirements

### Requirement: Envoi d'une demande de contact
Le système MUST permettre à un membre au profil complet d'envoyer une demande de contact pour un objet disponible dont il n'est pas propriétaire, avec un message facultatif de 500 caractères maximum. Avant l'envoi, le système MUST indiquer explicitement quelles coordonnées seront transmises au propriétaire (selon les réglages de partage du demandeur) et exiger que le demandeur le confirme. La demande est créée au statut « en attente ».

#### Scenario: Envoi valide
- **WHEN** un membre confirme l'envoi d'une demande pour l'objet d'un autre membre
- **THEN** une demande au statut « en attente » est créée et le propriétaire est notifié par email

#### Scenario: Consentement non confirmé
- **WHEN** un membre soumet la demande sans confirmer la transmission de ses coordonnées
- **THEN** le système refuse l'envoi et affiche une erreur

#### Scenario: Demande sur son propre objet
- **WHEN** un membre tente d'envoyer une demande pour son propre objet
- **THEN** le système refuse la demande

### Requirement: Coordonnées figées à l'envoi et à l'acceptation
Le système MUST enregistrer les coordonnées transmises au moment où elles le sont : celles du demandeur à l'envoi de la demande, celles du propriétaire à l'acceptation. Une modification ultérieure du profil ou des réglages de partage MUST ne pas changer les coordonnées déjà transmises, et MUST ne jamais exposer un canal que l'utilisateur ne partageait pas au moment de la transmission.

#### Scenario: Changement de réglages après l'envoi
- **WHEN** un demandeur ajoute le partage de son téléphone après avoir envoyé une demande qui ne transmettait que son email
- **THEN** le propriétaire continue de ne voir que l'email du demandeur pour cette demande

### Requirement: Notification du propriétaire
À la création d'une demande, le système MUST envoyer au propriétaire un email contenant le nom de l'objet, le pseudo et le quartier du demandeur, le message éventuel, les coordonnées transmises par le demandeur et un lien vers la demande dans l'application.

#### Scenario: Email de nouvelle demande
- **WHEN** une demande est créée
- **THEN** le propriétaire reçoit un email contenant ces informations et un lien vers la page « Demandes reçues »

### Requirement: Acceptation d'une demande
Le système MUST permettre au propriétaire d'accepter une demande en attente. La demande passe au statut « acceptée », les coordonnées que le propriétaire partage à ce moment sont transmises au demandeur, et le demandeur est notifié par email avec ces coordonnées.

#### Scenario: Acceptation
- **WHEN** le propriétaire accepte une demande en attente
- **THEN** la demande passe au statut « acceptée », le demandeur reçoit un email contenant les coordonnées partagées par le propriétaire, et ces coordonnées sont visibles par le demandeur dans « Mes demandes »

### Requirement: Refus d'une demande
Le système MUST permettre au propriétaire de refuser une demande en attente. La demande passe au statut « refusée ». Le demandeur MUST ne recevoir aucune notification ; le statut est visible dans « Mes demandes ».

#### Scenario: Refus
- **WHEN** le propriétaire refuse une demande en attente
- **THEN** la demande passe au statut « refusée », aucun email n'est envoyé au demandeur, et le demandeur voit ce statut dans « Mes demandes »

### Requirement: Décision définitive
Seul le propriétaire de l'objet MUST pouvoir accepter ou refuser une demande, et uniquement lorsqu'elle est en attente. Une demande acceptée, refusée ou annulée MUST ne plus pouvoir changer de statut.

#### Scenario: Décision sur une demande déjà traitée
- **WHEN** le propriétaire tente d'accepter une demande déjà refusée
- **THEN** le système refuse l'action et la demande conserve son statut

#### Scenario: Décision par un tiers
- **WHEN** un membre tente d'accepter une demande portant sur un objet qui ne lui appartient pas
- **THEN** le système refuse l'action

### Requirement: Annulation automatique
Le système MUST passer au statut « annulée » toute demande en attente dont l'objet est supprimé (par son propriétaire ou par la modération) ou dont le propriétaire ou le demandeur voit son compte supprimé ou suspendu. Aucune notification MUST être envoyée pour une annulation.

#### Scenario: Objet supprimé
- **WHEN** l'objet d'une demande en attente est supprimé
- **THEN** la demande passe au statut « annulée » sans notification

### Requirement: Page « Mes demandes »
Le système MUST fournir au membre la liste des demandes qu'il a envoyées, de la plus récente à la plus ancienne, avec pour chacune le nom de l'objet, le pseudo du propriétaire, la date et le statut. Pour une demande acceptée, les coordonnées transmises par le propriétaire MUST être affichées.

#### Scenario: Demande acceptée
- **WHEN** un membre consulte « Mes demandes » après l'acceptation d'une de ses demandes
- **THEN** il voit le statut « acceptée » et les coordonnées du propriétaire

#### Scenario: Demande annulée
- **WHEN** l'objet d'une de ses demandes a été supprimé
- **THEN** la demande apparaît avec le statut « annulée » et le nom de l'objet

### Requirement: Page « Demandes reçues »
Le système MUST fournir au membre la liste des demandes reçues sur ses objets, les demandes en attente en premier, avec pour chacune le nom de l'objet, le pseudo et le quartier du demandeur, le message, les coordonnées transmises, la date, le statut et, si elle est en attente, les actions « accepter » et « refuser ».

#### Scenario: Consultation des demandes reçues
- **WHEN** un membre ouvre « Demandes reçues »
- **THEN** il voit les demandes portant sur ses objets, avec les coordonnées transmises par chaque demandeur

### Requirement: Limite de demandes en attente
Le système MUST limiter à 5 le nombre de demandes en attente qu'un même membre peut avoir envoyées simultanément.

#### Scenario: Limite atteinte
- **WHEN** un membre ayant 5 demandes en attente tente d'en envoyer une sixième
- **THEN** le système refuse l'envoi et explique qu'il doit attendre une réponse à ses demandes en cours

### Requirement: Pas de demande en double
Le système MUST empêcher un membre d'envoyer plus d'une demande pour un même objet, quel que soit le statut de la demande existante (en attente, acceptée ou refusée).

#### Scenario: Nouvelle demande après un refus
- **WHEN** un membre dont la demande pour un objet a été refusée tente d'en envoyer une nouvelle pour ce même objet
- **THEN** le système refuse l'envoi, et la fiche de l'objet affiche le statut de la demande existante à la place du bouton de demande
