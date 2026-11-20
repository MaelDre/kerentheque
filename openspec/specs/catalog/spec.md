# catalog Specification

## Purpose

Permet à chacun de découvrir les objets prêtables de la zone, de les rechercher et de les filtrer, sans exposer d'autre information sur les propriétaires que leur pseudo et leur quartier.

## Requirements

### Requirement: Consultation du catalogue
Le système MUST afficher, y compris aux visiteurs non connectés, la liste des objets disponibles : objets non supprimés dont le propriétaire a un compte actif (ni supprimé, ni suspendu). Chaque entrée MUST afficher le nom de l'objet, sa catégorie et le quartier du propriétaire. Pour un membre connecté, chaque entrée MUST en plus afficher le pseudo du propriétaire. Pour un visiteur non connecté, le pseudo du propriétaire MUST NOT apparaître nulle part dans la page. Les objets les plus récents apparaissent en premier, et la liste est paginée par 20 objets.

#### Scenario: Visiteur non connecté
- **WHEN** un visiteur non connecté ouvre le catalogue
- **THEN** il voit la liste des objets disponibles, avec leur nom, leur catégorie et le quartier du propriétaire
- **AND** le pseudo d'aucun propriétaire n'apparaît dans la page

#### Scenario: Membre connecté
- **WHEN** un membre connecté ouvre le catalogue
- **THEN** chaque objet affiche le pseudo et le quartier de son propriétaire

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
Le système MUST fournir une page de détail par objet, affichant son nom, sa catégorie, sa description et le quartier du propriétaire. Pour un membre connecté, la fiche MUST en plus afficher le pseudo du propriétaire. Pour un membre connecté qui n'est pas le propriétaire, la fiche MUST proposer l'envoi d'une demande de contact, ou indiquer le statut de sa demande existante. Pour un visiteur non connecté, elle MUST proposer de se connecter, et le pseudo du propriétaire MUST NOT apparaître nulle part dans la page.

#### Scenario: Fiche vue par un visiteur
- **WHEN** un visiteur non connecté ouvre la fiche d'un objet
- **THEN** il voit le nom, la catégorie, la description de l'objet et le quartier du propriétaire, ainsi qu'une invitation à se connecter pour contacter le prêteur
- **AND** le pseudo du propriétaire n'apparaît pas dans la page

#### Scenario: Fiche vue par un membre
- **WHEN** un membre connecté qui n'est pas le propriétaire ouvre la fiche d'un objet
- **THEN** il voit le pseudo et le quartier du propriétaire, et peut lui envoyer une demande de contact

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

### Requirement: Compteur d'objets et prochain palier
Le système MUST afficher sur l'accueil du catalogue, à tous les visiteurs connectés ou non, un compteur du nombre d'objets disponibles, c'est-à-dire des objets qui apparaissent dans le catalogue (non supprimés, propriétaire au compte actif). Ce nombre MUST être indépendant de la recherche, des filtres et de la page consultée. Il MUST être affiché même s'il vaut 0, avec un libellé accordé au singulier pour 0 et 1 objet et au pluriel au-delà.

Sous le compteur, le système MUST afficher un bloc qui invite à ajouter un objet. Il contient un bouton « Ajouter un objet » : pour un membre connecté, le bouton MUST mener au formulaire d'ajout d'un objet ; pour un visiteur non connecté, il MUST mener à la page de connexion.

Les paliers sont, dans l'ordre : 25, 50, 100, 200, 300, 400, 500, 700, 1000. Le prochain palier est le plus petit palier strictement supérieur au nombre d'objets disponibles. Tant qu'il existe un prochain palier, le bloc MUST afficher :
- le prochain palier (« Prochain palier : N objets ») ;
- le pourcentage atteint, égal au nombre d'objets divisé par le prochain palier, arrondi à l'entier inférieur ;
- une barre de progression accessible, de 0 au prochain palier, qui reflète ce pourcentage ;
- le nombre d'objets manquants pour l'atteindre, accordé au singulier ou au pluriel ;
- une mention « Bientôt atteint » lorsque le pourcentage est d'au moins 80 %.

À partir de 1000 objets disponibles, il n'existe plus de prochain palier : le bloc MUST alors masquer le palier, le pourcentage, la barre et le nombre manquant, et ne garder qu'une phrase d'invitation et le bouton « Ajouter un objet ».

#### Scenario: Aucun objet
- **WHEN** le catalogue ne contient aucun objet disponible
- **THEN** l'accueil affiche « 0 objet disponible »
- **AND** le bloc indique « Prochain palier : 25 objets », 0 %, et qu'il manque 25 objets

#### Scenario: Un seul objet
- **WHEN** le catalogue contient 1 objet disponible
- **THEN** l'accueil affiche « 1 objet disponible », au singulier

#### Scenario: Approche d'un palier
- **WHEN** le catalogue contient 87 objets disponibles
- **THEN** le bloc indique « Prochain palier : 100 objets », 87 %, qu'il manque 13 objets, et affiche la mention « Bientôt atteint »

#### Scenario: Loin d'un palier
- **WHEN** le catalogue contient 120 objets disponibles
- **THEN** le bloc indique « Prochain palier : 200 objets », 60 %, et n'affiche pas la mention « Bientôt atteint »

#### Scenario: Plus qu'un objet manquant
- **WHEN** le catalogue contient 24 objets disponibles
- **THEN** le bloc indique qu'il manque 1 objet, au singulier

#### Scenario: Palier tout juste atteint
- **WHEN** le catalogue contient exactement 25 objets disponibles
- **THEN** le bloc indique « Prochain palier : 50 objets » et 50 %

#### Scenario: Dernier palier atteint
- **WHEN** le catalogue contient 1000 objets disponibles ou plus
- **THEN** l'accueil affiche le compteur
- **AND** le bloc n'affiche ni palier, ni pourcentage, ni barre de progression, mais garde une phrase d'invitation et le bouton « Ajouter un objet »

#### Scenario: Objets non disponibles exclus du compteur
- **WHEN** un objet est supprimé, ou que le compte de son propriétaire est suspendu
- **THEN** il n'est pas compté dans le compteur de l'accueil

#### Scenario: Compteur indépendant des filtres
- **WHEN** un visiteur effectue une recherche ou applique un filtre qui réduit la liste affichée
- **THEN** le compteur affiche toujours le nombre total d'objets disponibles

#### Scenario: Bouton pour un membre connecté
- **WHEN** un membre connecté clique sur « Ajouter un objet » depuis l'accueil
- **THEN** il arrive sur le formulaire d'ajout d'un objet

#### Scenario: Bouton pour un visiteur non connecté
- **WHEN** un visiteur non connecté clique sur « Ajouter un objet » depuis l'accueil
- **THEN** il arrive sur la page de connexion
