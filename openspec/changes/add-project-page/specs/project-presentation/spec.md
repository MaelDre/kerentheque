## Purpose

Présente Kerentheque à ses visiteurs : une page qui explique l'esprit du projet, son fonctionnement, qui le porte et la suite prévue, ainsi que les points d'accès qui y mènent depuis le reste du site.

## ADDED Requirements

### Requirement: Page de présentation du projet
Le système MUST servir une page « Le projet » à l'adresse `/le-projet/`, accessible à tout visiteur, connecté ou non, sans redirection vers la connexion. La page MUST présenter, dans cet ordre, quatre sections titrées : « Pourquoi ? », « Comment ça marche ? », « Qui sommes-nous ? » et « Les prochaines étapes ».

#### Scenario: Visiteur non connecté
- **WHEN** un visiteur non connecté ouvre `/le-projet/`
- **THEN** la page « Le projet » s'affiche directement, sans passer par la page de connexion

#### Scenario: Membre connecté
- **WHEN** un membre connecté ouvre `/le-projet/`
- **THEN** la page « Le projet » s'affiche avec le même en-tête que les autres pages pour un membre connecté

#### Scenario: Plan de la page
- **WHEN** un visiteur lit la page « Le projet »
- **THEN** il trouve, dans cet ordre, les sections « Pourquoi ? », « Comment ça marche ? », « Qui sommes-nous ? » et « Les prochaines étapes »

### Requirement: Accès depuis le menu
L'en-tête de toutes les pages MUST contenir une entrée « Le projet » menant à la page de présentation, que le visiteur soit connecté ou non. Cette entrée MUST être visible sans ouvrir de sous-menu et MUST NOT utiliser le style d'action principale.

#### Scenario: Menu d'un visiteur non connecté
- **WHEN** un visiteur non connecté affiche une page quelconque
- **THEN** l'en-tête propose l'entrée « Le projet » à côté de « Se connecter »

#### Scenario: Menu d'un membre connecté
- **WHEN** un membre connecté affiche une page quelconque
- **THEN** l'en-tête propose l'entrée « Le projet » directement, hors du menu « Mon compte »

### Requirement: Accès depuis le pied de page
Le pied de page de toutes les pages MUST contenir un lien « Le projet » menant à la page de présentation, à côté des liens vers les mentions légales et la page de confidentialité.

#### Scenario: Lien en pied de page
- **WHEN** un visiteur, connecté ou non, fait défiler une page jusqu'en bas
- **THEN** le pied de page propose un lien « Le projet » à côté de « Mentions légales » et « Confidentialité »

### Requirement: Bandeau de présentation sur l'accueil
La page d'accueil MUST afficher, pour tout visiteur, un bandeau qui met en avant le projet par une phrase courte et propose un bouton menant à la page « Le projet ». Le bandeau MUST rester léger : une seule phrase, un seul bouton, sans image. Le bouton du bandeau MUST être présenté comme une action secondaire, l'action principale de l'accueil restant le bouton de filtrage du catalogue. Le bandeau MUST NOT être affiché sur les autres pages.

#### Scenario: Affichage du bandeau
- **WHEN** un visiteur, connecté ou non, ouvre la page d'accueil
- **THEN** un bandeau présente le projet en une phrase et propose un bouton menant à `/le-projet/`

#### Scenario: Hiérarchie des actions préservée
- **WHEN** un visiteur affiche la page d'accueil
- **THEN** le bouton du bandeau est présenté comme une action secondaire et « Filtrer » reste la seule action principale de la page

#### Scenario: Bandeau limité à l'accueil
- **WHEN** un visiteur ouvre une autre page que l'accueil, par exemple le détail d'un objet ou la page « Le projet »
- **THEN** aucun bandeau de présentation n'est affiché
