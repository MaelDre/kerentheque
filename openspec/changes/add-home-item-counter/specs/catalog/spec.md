## ADDED Requirements

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
