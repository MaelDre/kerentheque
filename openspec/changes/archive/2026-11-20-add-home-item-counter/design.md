## Context

L'accueil est la vue `items.views.catalog`, rendue par `items/templates/items/catalog.html` : titre, bandeau « Découvrir le projet », filtres, liste paginée. Le site est entièrement rendu côté serveur (Django + Pico CSS + design system dans `design-system/tokens.css`). Le seul JavaScript est `static/js/protected-email.js`. Les éléments déjà disponibles :
- `Item.objects.available()`, la définition des objets visibles dans le catalogue ;
- `page.paginator.count`, qui compte les objets **après** recherche et filtres, donc inutilisable pour le compteur (cf. spec, « Compteur indépendant des filtres ») ;
- `LANGUAGE_CODE = "fr-fr"`, sans séparateur de milliers activé globalement.

La maquette `_elements_de_travail/kerentheque-compteur.html` sert de référence visuelle. Sa logique JS (`fetch('/api/stats')`, animation du compteur) n'est pas reprise.

## Goals / Non-Goals

**Goals:**
- Garder la logique de palier dans une fonction Python pure, testable sans base de données ni template.
- Ne rien ajouter côté client : pas de JS, pas d'API.

**Non-Goals:**
- Cache du compteur.
- Paliers configurables (admin, settings) : ils sont en dur, comme demandé.
- Retour vers le formulaire d'ajout après connexion (`next` à travers le lien magique) : change séparé.

## Decisions

### 1. Rendu serveur plutôt qu'API + JS
Le nombre et le palier sont calculés dans la vue et passés au template. La maquette prévoyait un appel `fetch` parce qu'elle était autonome. Ici, Django a déjà la donnée au moment du rendu : une API ajouterait une URL publique, du JS et un état de chargement, sans aucun bénéfice.

### 2. Module `items/milestones.py` pour la logique de palier
Il contient la constante `MILESTONES = (25, 50, 100, 200, 300, 400, 500, 700, 1000)`, et une fonction `milestone_progress(count)` qui renvoie `None` quand `count >= 1000`, et sinon un petit objet immuable (dataclass) avec `target`, `percent` (division entière `count * 100 // target`), `missing` et `is_close` (`percent >= 80`).
Pourquoi un module dédié plutôt que `services.py` : `services.py` contient des opérations qui modifient des données (`delete_item`). Le palier est un calcul pur, sans dépendance à Django. Un module séparé est plus lisible et se teste avec de simples `assert`.
*Alternative écartée :* calculer dans le template avec des filtres : illisible, et non testable unitairement.

### 3. Comptage séparé dans la vue
La vue `catalog` ajoute `item_count = Item.objects.available().count()` et `milestone = milestone_progress(item_count)` au contexte. C'est une requête `COUNT` en plus, indépendante du queryset filtré.

### 4. Fragment de template `items/home_stats.html`
Les deux blocs sont dans un fragment inclus dans `catalog.html`, entre le bandeau projet et le formulaire de filtres. Le template du catalogue reste ainsi lisible, et le fragment pourra être déplacé facilement.

### 5. Accords singulier/pluriel dans le template, sans `pluralize`
Le filtre `pluralize` de Django met le pluriel pour 0 (règle anglaise). La spec demande « 0 objet disponible », donc on utilise un `{% if item_count > 1 %}` explicite, et de même pour `missing`. Les nombres sont formatés avec `floatformat:"g"`, qui applique le séparateur de milliers de la locale française (« 1 000 ») sans activer `USE_THOUSAND_SEPARATOR` sur tout le site.

### 6. Barre de progression : élément natif `<progress>`
`<progress max="100" value="{{ milestone.percent }}" aria-label="…">` est annoncé nativement par les lecteurs d'écran, et Pico le style déjà. Sa couleur est forcée à `var(--brand)`, unie.
*Alternative écartée :* le `div role="progressbar"` de la maquette : il faut gérer à la main les attributs ARIA et la largeur en style inline, sans bénéfice.

### 7. Hiérarchie des boutons
- « Ajouter un objet » : bouton principal Pico (`role="button"`, fond `brand`). Il pointe vers `items:create` si l'utilisateur est connecté, et vers `accounts:login` sinon.
- « Filtrer » : passe en `class="secondary"`, comme le bouton du bandeau projet.

### 8. Adaptation visuelle au design system
| Maquette | Implémentation |
|---|---|
| emojis 📦 ➕ | supprimés (pas de jeu d'icônes choisi) |
| ombres portées | cartes `surface-raised` + filet `border`, `radius-lg` |
| dégradé et reflet animé de la barre | barre unie `brand`, sans animation |
| bordure dorée `is-close` | pastille « Bientôt atteint » : fond `accent`, texte `ink`, `radius-pill` |
| chiffre en vert, très gros | `font-display` 700, couleur `brand` (contraste suffisant sur `surface-raised`) |
| couleurs en dur | tokens uniquement |

## Risks / Trade-offs

- [Un chiffre bas peut donner une impression de plateforme vide] → C'est un choix assumé. Le bloc de palier présente ce chiffre comme un objectif collectif.
- [Le visiteur anonyme arrive sur la connexion, puis revient sur l'accueil plutôt que sur le formulaire] → Il lui faut un clic de plus, en attendant le change sur `next`.
- [Hauteur ajoutée avant les filtres sur mobile] → Blocs compacts (padding `space-4`), et compteur en ligne (chiffre + libellé côte à côte).
- [Requête `COUNT` à chaque affichage de l'accueil] → Négligeable au volume de l'alpha. Un cache pourra être ajouté si besoin, sans changer la spec.
