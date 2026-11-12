## Why

Sur mobile, les éléments du formulaire de filtres du catalogue sont empilés sans aucun espace vertical : chaque libellé (« Catégorie », « Quartier ») est collé au champ du dessus, et le bouton « Filtrer » touche le sélecteur « Quartier ». Le formulaire paraît tassé et il est moins facile de voir quel libellé va avec quel champ.

## What Changes

- Ajouter un espacement vertical entre les groupes du formulaire de filtres (Rechercher, Catégorie, Quartier, bouton Filtrer) quand ils sont empilés (largeur < 768 px).
- Aucun changement sur écran large : les éléments y tiennent sur une seule ligne, l'alignement corrigé dans `align-catalog-filter-button` reste intact.

Cause identifiée : la grille `.filters` déclare `gap: 0 var(--space-4)`, c'est-à-dire 0 entre les lignes et 16 px entre les colonnes. Le formulaire porte `role="search"`, et Pico retire dans ce cas la marge basse des champs, qui assurait d'habitude cet espacement. Résultat : il ne reste plus rien entre les lignes.

## Capabilities

### New Capabilities

_Aucune._

### Modified Capabilities

_Aucune — correction purement visuelle, aucune exigence de spec ne change (`skip_specs: true`)._

## Impact

- `static/css/site.css` : l'espacement entre lignes de la grille `.filters` passe de `0` à `var(--space-3)` (12 px), comme pour `.project-banner` qui utilise déjà `gap: var(--space-3) var(--space-4)`.
- Aucun template, aucune vue, aucune dépendance touchés.
