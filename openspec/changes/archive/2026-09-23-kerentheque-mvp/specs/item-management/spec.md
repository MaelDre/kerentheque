## Purpose

Permet à chaque membre de déclarer, modifier et retirer les objets qu'il accepte de prêter, afin qu'ils apparaissent dans le catalogue.

## ADDED Requirements

### Requirement: Ajout d'un objet
Le système MUST permettre à un membre au profil complet d'ajouter un objet prêtable avec un nom (obligatoire, 100 caractères maximum), une catégorie choisie parmi les catégories actives (obligatoire) et une description (facultative, 2000 caractères maximum). Tout objet ajouté est public et apparaît immédiatement dans le catalogue.

#### Scenario: Ajout valide
- **WHEN** un membre soumet un nom et une catégorie active
- **THEN** l'objet est créé, rattaché à ce membre, et visible dans le catalogue

#### Scenario: Champ obligatoire manquant
- **WHEN** un membre soumet le formulaire sans nom ou sans catégorie
- **THEN** le système refuse la création et affiche une erreur

#### Scenario: Visiteur non connecté
- **WHEN** un visiteur non connecté tente d'accéder au formulaire d'ajout
- **THEN** le système le redirige vers la page de connexion

### Requirement: Liste de mes objets
Le système MUST fournir au membre une page listant ses propres objets non supprimés, avec pour chacun un accès à la modification et à la suppression.

#### Scenario: Consultation de mes objets
- **WHEN** un membre ouvre la page « Mes objets »
- **THEN** il voit tous ses objets non supprimés, et uniquement les siens

### Requirement: Modification d'un objet
Le système MUST permettre au propriétaire d'un objet d'en modifier le nom, la catégorie et la description, avec les mêmes règles de validation qu'à l'ajout. Seul le propriétaire MUST pouvoir modifier son objet.

#### Scenario: Modification par le propriétaire
- **WHEN** le propriétaire modifie la description de son objet
- **THEN** la nouvelle description est affichée dans le catalogue

#### Scenario: Tentative de modification par un tiers
- **WHEN** un membre tente de modifier un objet dont il n'est pas propriétaire
- **THEN** le système refuse l'accès

### Requirement: Suppression d'un objet
Le système MUST permettre au propriétaire de supprimer son objet après confirmation. L'objet supprimé MUST disparaître du catalogue et de « Mes objets », mais son nom MUST rester lisible dans l'historique des demandes qui le concernent. Toutes les demandes en attente sur cet objet MUST passer au statut « annulée », sans notification aux demandeurs.

#### Scenario: Suppression d'un objet sans demande
- **WHEN** le propriétaire confirme la suppression d'un objet
- **THEN** l'objet n'apparaît plus dans le catalogue ni dans « Mes objets »

#### Scenario: Suppression d'un objet avec demandes en attente
- **WHEN** le propriétaire supprime un objet qui a des demandes en attente
- **THEN** ces demandes passent au statut « annulée », aucun email n'est envoyé aux demandeurs, et elles restent visibles avec le nom de l'objet dans « Mes demandes » des demandeurs

#### Scenario: Demandes déjà traitées
- **WHEN** le propriétaire supprime un objet qui a des demandes acceptées ou refusées
- **THEN** ces demandes conservent leur statut
