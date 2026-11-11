## MODIFIED Requirements

### Requirement: Suppression de compte
Le système MUST permettre à l'utilisateur de supprimer son compte après confirmation. La suppression MUST effacer son email, son téléphone, son pseudo et son quartier, retirer tous ses objets du catalogue, et annuler toutes les demandes en attente qu'il a envoyées ou reçues. Elle MUST aussi effacer les textes libres qu'il a rédigés et qui sont liés à son activité de prêt : la description de ses objets et le message de chaque demande de contact qu'il a envoyée. Elle MUST conserver le nom de ses objets (affiché dans l'historique des autres membres) et les motifs des signalements qu'il a rédigés (nécessaires à la modération). Dans l'historique des autres utilisateurs, il MUST apparaître comme « Utilisateur supprimé ».

#### Scenario: Suppression confirmée
- **WHEN** un utilisateur confirme la suppression de son compte
- **THEN** ses données personnelles sont effacées, ses objets disparaissent du catalogue, ses demandes en attente sont annulées et sa session est fermée

#### Scenario: Effacement des textes libres
- **WHEN** un utilisateur qui a publié des objets avec une description et envoyé des demandes de contact avec un message supprime son compte
- **THEN** la description de ses objets et le message de ses demandes sont vides, le nom de ses objets reste visible dans l'historique des autres membres, et ceux-ci ne voient plus son message

#### Scenario: Conservation des signalements
- **WHEN** un utilisateur qui a rédigé un signalement supprime son compte
- **THEN** le signalement et son motif restent consultables par les administrateurs, avec un auteur affiché comme « Utilisateur supprimé »

#### Scenario: Reconnexion après suppression
- **WHEN** une personne demande un lien de connexion avec l'email d'un compte supprimé
- **THEN** le système la traite comme une nouvelle inscription, sans lien avec l'ancien compte

### Requirement: Pages légales
Le système MUST fournir, accessibles sans connexion, une page de mentions légales et une page de politique de confidentialité dont le contenu respecte la capability `legal-information`.

#### Scenario: Accès aux pages légales
- **WHEN** un visiteur ouvre le lien vers la politique de confidentialité depuis n'importe quelle page
- **THEN** la page s'affiche sans connexion requise
