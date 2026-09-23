## Purpose

Permet à chacun de découvrir les objets prêtables de la zone, de les rechercher et de les filtrer, sans exposer d'autre information sur les propriétaires que leur pseudo et leur quartier.

## ADDED Requirements

### Requirement: Consultation du catalogue
Le système MUST afficher, y compris aux visiteurs non connectés, la liste des objets disponibles : objets non supprimés dont le propriétaire a un compte actif (ni supprimé, ni suspendu). Chaque entrée MUST afficher le nom de l'objet, sa catégorie, le pseudo et le quartier du propriétaire. Les objets les plus récents apparaissent en premier, et la liste est paginée par 20 objets.

#### Scenario: Visiteur non connecté
- **WHEN** un visiteur non connecté ouvre le catalogue
- **THEN** il voit la liste des objets disponibles

#### Scenario: Objet supprimé
- **WHEN** un objet a été supprimé par son propriétaire ou par la modération
- **THEN** il n'apparaît plus dans le catalogue

#### Scenario: Propriétaire suspendu
- **WHEN** le compte du propriétaire d'un objet est suspendu
- **THEN** ses objets n'apparaissent plus dans le catalogue

### Requirement: Recherche texte
Le système MUST permettre de rechercher des objets par un texte libre, comparé sans distinction de casse au nom et à la description des objets.

#### Scenario: Recherche avec résultats
- **WHEN** un visiteur recherche « perceuse »
- **THEN** le catalogue n'affiche que les objets dont le nom ou la description contient « perceuse »

#### Scenario: Recherche sans résultat
- **WHEN** aucune correspondance n'est trouvée
- **THEN** le catalogue affiche un message indiquant qu'aucun objet ne correspond

### Requirement: Filtres par catégorie et par quartier
Le système MUST permettre de filtrer le catalogue par catégorie et par quartier du propriétaire. Les filtres et la recherche texte MUST pouvoir être combinés, et ils sont conservés dans l'URL pour qu'une recherche puisse être partagée.

#### Scenario: Combinaison de filtres
- **WHEN** un visiteur filtre sur la catégorie « Bricolage » et le quartier « Centre » avec la recherche « scie »
- **THEN** le catalogue n'affiche que les objets remplissant les trois critères

### Requirement: Fiche d'un objet
Le système MUST fournir une page de détail par objet, affichant son nom, sa catégorie, sa description, le pseudo et le quartier du propriétaire. Pour un membre connecté qui n'est pas le propriétaire, la fiche MUST proposer l'envoi d'une demande de contact, ou indiquer le statut de sa demande existante. Pour un visiteur non connecté, elle MUST proposer de se connecter.

#### Scenario: Fiche vue par un visiteur
- **WHEN** un visiteur non connecté ouvre la fiche d'un objet
- **THEN** il voit les informations publiques de l'objet et une invitation à se connecter pour contacter le propriétaire

#### Scenario: Fiche vue par le propriétaire
- **WHEN** le propriétaire ouvre la fiche de son propre objet
- **THEN** aucune demande de contact n'est proposée, et un accès à la modification est affiché

#### Scenario: Objet indisponible
- **WHEN** quelqu'un ouvre l'adresse d'un objet supprimé ou appartenant à un compte suspendu
- **THEN** le système affiche une page « objet introuvable »

### Requirement: Affichage responsive
Toutes les pages de l'application MUST être utilisables sur un écran de téléphone (largeur de 360 px) comme sur ordinateur, sans défilement horizontal.

#### Scenario: Consultation sur mobile
- **WHEN** un visiteur ouvre le catalogue sur un écran de 360 px de large
- **THEN** la liste, la recherche et les filtres sont lisibles et utilisables sans défilement horizontal
