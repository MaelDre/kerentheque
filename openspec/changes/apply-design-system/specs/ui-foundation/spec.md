## Purpose

Définit le socle commun de l'interface de Kerentheque : une identité visuelle unique appliquée à toutes les pages, et les exigences d'accessibilité qui rendent l'application utilisable par tous les habitants, au doigt comme au clavier.

## ADDED Requirements

### Requirement: Identité visuelle commune
Le système MUST afficher toutes ses pages avec les couleurs, les polices et les formes définies par le design system de l'application. Les titres MUST utiliser la police de titre du design system et le texte courant sa police de lecture. Les polices MUST être servies par l'application elle-même, sans appel à un service tiers.

#### Scenario: Ouverture d'une page quelconque
- **WHEN** un visiteur ouvre n'importe quelle page du site, y compris les pages d'erreur 404 et 500
- **THEN** la page s'affiche avec le fond, les couleurs de texte et les polices du design system

#### Scenario: Aucune requête vers un service de polices tiers
- **WHEN** une page est chargée
- **THEN** toutes les polices proviennent du domaine de l'application

### Requirement: Thème clair unique
Le système MUST toujours s'afficher en thème clair, quelle que soit la préférence de thème du système d'exploitation ou du navigateur du visiteur.

#### Scenario: Visiteur en mode sombre
- **WHEN** un visiteur dont l'appareil est réglé en mode sombre ouvre une page
- **THEN** la page s'affiche en thème clair, avec les mêmes couleurs que pour un appareil en mode clair

### Requirement: Cibles tactiles suffisantes
Tout bouton, lien présenté comme un bouton, champ de saisie, liste déroulante et élément de menu MUST offrir une zone cliquable d'au moins 44px de hauteur.

#### Scenario: Bouton sur mobile
- **WHEN** un visiteur affiche un formulaire sur un écran de téléphone
- **THEN** chaque bouton et chaque champ du formulaire mesure au moins 44px de haut

#### Scenario: Menu du compte
- **WHEN** un membre ouvre le menu « Mon compte »
- **THEN** chaque entrée du menu, y compris « Se déconnecter », offre une zone cliquable d'au moins 44px de haut

### Requirement: Focus clavier visible
Tout élément interactif MUST afficher, lorsqu'il reçoit le focus au clavier, un anneau plein de 2px dans la couleur principale, décalé de 2px de l'élément, visible sur toutes les surfaces du design system.

#### Scenario: Navigation au clavier
- **WHEN** un visiteur parcourt une page avec la touche Tab
- **THEN** l'élément qui a le focus est entouré d'un anneau visible, et un seul élément à la fois porte cet anneau

### Requirement: Taille du texte de saisie
Le texte saisi dans un champ de formulaire MUST s'afficher à 16px minimum, afin d'éviter le zoom automatique des navigateurs mobiles.

#### Scenario: Saisie sur téléphone
- **WHEN** un visiteur touche un champ de saisie sur un téléphone
- **THEN** le texte du champ s'affiche à 16px ou plus et la page ne zoome pas automatiquement

### Requirement: Contrastes suffisants
Tout texte MUST présenter un contraste d'au moins 4,5:1 avec son fond. Les bordures des champs, cases à cocher et boutons secondaires MUST présenter un contraste d'au moins 3:1 avec leur fond.

#### Scenario: Texte secondaire
- **WHEN** une page affiche une métadonnée (catégorie, quartier, date) en texte secondaire
- **THEN** ce texte présente un contraste d'au moins 4,5:1 avec le fond sur lequel il est posé

#### Scenario: Bordure d'un champ
- **WHEN** un formulaire affiche un champ de saisie vide
- **THEN** la bordure du champ présente un contraste d'au moins 3:1 avec le fond

### Requirement: État jamais porté par la seule couleur
Le système MUST accompagner toute information d'état (statut d'une demande, message de succès ou d'erreur, erreur de champ, action de suppression) d'un libellé textuel explicite. La couleur peut renforcer le message mais MUST NOT être le seul moyen de le transmettre.

#### Scenario: Statut d'une demande de contact
- **WHEN** un membre consulte la liste de ses demandes envoyées ou reçues
- **THEN** chaque demande affiche son statut sous forme de pastille contenant le mot du statut (par exemple « En attente », « Acceptée »)

#### Scenario: Erreur de formulaire
- **WHEN** un formulaire est renvoyé avec une erreur sur un champ
- **THEN** le message d'erreur est affiché en texte à côté du champ concerné, en plus de la couleur d'erreur

### Requirement: Hiérarchie des actions
Chaque page MUST présenter au plus une action principale, mise en avant dans la couleur principale. Dans une liste d'éléments indépendants, comme les demandes reçues, cette limite s'applique à chaque élément. Les autres actions MUST être présentées comme des actions secondaires, et la navigation générale MUST NOT utiliser le style d'action principale. Les actions qui suppriment des données MUST être présentées avec le style « danger » et un libellé qui nomme explicitement la suppression.

#### Scenario: Formulaire avec annulation
- **WHEN** un membre affiche le formulaire d'ajout ou de modification d'un objet
- **THEN** le bouton d'enregistrement est la seule action principale, et le lien « Annuler » est présenté comme une action secondaire

#### Scenario: Page de connexion
- **WHEN** un visiteur non connecté ouvre la page de connexion
- **THEN** le bouton d'envoi du lien de connexion est la seule action principale de la page, et le lien « Se connecter » de l'en-tête n'utilise pas le style principal

#### Scenario: Confirmation de suppression
- **WHEN** un membre arrive sur l'écran de confirmation de suppression d'un objet ou de son compte
- **THEN** le bouton de suppression est présenté avec le style « danger » et un libellé qui nomme la suppression, et le lien « Annuler » est une action secondaire

#### Scenario: Réponse à une demande reçue
- **WHEN** un membre consulte une demande de contact en attente qu'il a reçue
- **THEN** « Accepter » est l'action principale et « Refuser » une action secondaire
