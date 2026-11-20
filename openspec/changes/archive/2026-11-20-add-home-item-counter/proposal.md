## Why

Pendant l'alpha, le catalogue grandit seulement si des habitants proposent des objets. Rien sur l'accueil ne montre aujourd'hui l'état de la plateforme ni n'invite explicitement à prêter. Un compteur d'objets et un objectif chiffré (le prochain palier) rendent la progression visible et donnent une raison concrète d'ajouter un objet, même quand le catalogue est encore petit.

## What Changes

- Ajout sur l'accueil (le catalogue), sous le bandeau « Découvrir le projet » et au-dessus des filtres, de deux blocs visibles par tous les visiteurs, connectés ou non :
  - **Compteur** : nombre d'objets disponibles (ceux qui apparaissent dans le catalogue), accordé au singulier ou au pluriel, affiché même s'il vaut 0 ;
  - **Prochain palier** : titre « Prochain palier : N objets », pourcentage atteint, barre de progression, nombre d'objets manquants et bouton « Ajouter un objet ». Les paliers sont fixes : 25, 50, 100, 200, 300, 400, 500, 700, 1000. À partir de 80 %, une pastille « Bientôt atteint » s'affiche.
- À partir de 1000 objets, il n'y a plus de palier : la partie palier est masquée et le bloc se réduit à une phrase d'invitation avec le bouton.
- Le bouton « Ajouter un objet » devient l'action principale de l'accueil. Il mène au formulaire d'ajout pour un membre connecté, et à la page de connexion pour un visiteur non connecté. Le bouton « Filtrer » passe en style secondaire.
- Le visuel reprend la maquette `_elements_de_travail/kerentheque-compteur.html`, adaptée au design system : tokens uniquement, sans emoji, dégradé, ombre ni animation.

Hors périmètre : le retour automatique vers le formulaire d'ajout après connexion. Le lien magique ne conserve pas aujourd'hui le paramètre `next`, ce sera traité dans un change séparé.

## Capabilities

### New Capabilities

_Aucune._

### Modified Capabilities

- `catalog` : ajout d'une exigence « Compteur d'objets et prochain palier » sur l'accueil du catalogue.

## Impact

- `items` : calcul du palier (fonction Python testable), vue `catalog` (nombre d'objets disponibles dans le contexte), template `catalog.html`.
- `static/css/site.css` : styles des deux blocs, basés sur les tokens.
- Une requête `COUNT` supplémentaire par affichage de l'accueil, négligeable à l'échelle de l'alpha.
- Aucune migration, aucune nouvelle dépendance, aucune nouvelle URL, aucun JavaScript.
