# moderation Specification

## Purpose

Donne aux membres un moyen de signaler les contenus ou comportements problématiques, et aux administrateurs les outils pour gérer les listes de référence (catégories, quartiers) et agir sur les objets et les comptes.

## Requirements

### Requirement: Signalement d'un objet ou d'un utilisateur
Le système MUST permettre à un membre connecté de signaler un objet ou le propriétaire d'un objet, avec un motif obligatoire (1000 caractères maximum). Un membre MUST ne pas pouvoir se signaler lui-même ni signaler ses propres objets.

#### Scenario: Signalement d'un objet
- **WHEN** un membre signale un objet en indiquant un motif
- **THEN** le signalement est enregistré et le membre voit une confirmation

#### Scenario: Motif manquant
- **WHEN** un membre soumet un signalement sans motif
- **THEN** le système refuse le signalement et affiche une erreur

### Requirement: Traitement des signalements
Le système MUST permettre aux administrateurs de consulter les signalements (auteur, cible, motif, date), du plus récent au plus ancien, et de marquer un signalement comme traité.

#### Scenario: Consultation des signalements
- **WHEN** un administrateur ouvre la liste des signalements
- **THEN** il voit les signalements non traités, avec un accès direct à l'objet ou à l'utilisateur concerné

### Requirement: Retrait d'un objet par la modération
Le système MUST permettre à un administrateur de supprimer un objet. Les effets sont les mêmes qu'une suppression par le propriétaire : l'objet disparaît du catalogue et ses demandes en attente sont annulées.

#### Scenario: Objet retiré
- **WHEN** un administrateur supprime un objet signalé
- **THEN** l'objet disparaît du catalogue et ses demandes en attente passent au statut « annulée »

### Requirement: Suspension d'un compte
Le système MUST permettre à un administrateur de suspendre et de réactiver un compte. Un compte suspendu MUST ne plus pouvoir se connecter, ses objets MUST disparaître du catalogue, et ses demandes en attente (envoyées et reçues) MUST être annulées.

#### Scenario: Suspension
- **WHEN** un administrateur suspend un compte
- **THEN** l'utilisateur ne peut plus se connecter, ses objets ne sont plus visibles dans le catalogue et ses demandes en attente sont annulées

#### Scenario: Réactivation
- **WHEN** un administrateur réactive un compte suspendu
- **THEN** l'utilisateur peut à nouveau se connecter et ses objets non supprimés réapparaissent dans le catalogue

### Requirement: Gestion des catégories et des quartiers
Le système MUST permettre aux administrateurs de créer, renommer, réordonner et désactiver des catégories et des quartiers. Une catégorie ou un quartier désactivé MUST ne plus être proposé dans les formulaires, mais les objets et profils qui l'utilisent déjà MUST continuer de l'afficher. Une catégorie ou un quartier MUST ne pas pouvoir être supprimé s'il est utilisé.

#### Scenario: Désactivation d'une catégorie utilisée
- **WHEN** un administrateur désactive une catégorie utilisée par des objets
- **THEN** la catégorie n'est plus proposée à l'ajout d'un objet, et les objets existants conservent cette catégorie

#### Scenario: Suppression d'un quartier utilisé
- **WHEN** un administrateur tente de supprimer un quartier choisi par au moins un utilisateur
- **THEN** le système refuse la suppression

### Requirement: Accès restreint à l'administration
L'interface d'administration MUST n'être accessible qu'aux comptes disposant des droits d'administrateur.

#### Scenario: Membre sans droits
- **WHEN** un membre sans droits d'administrateur tente d'accéder à l'interface d'administration
- **THEN** le système refuse l'accès
