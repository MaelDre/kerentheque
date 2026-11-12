## Why

Sur le catalogue, le bouton « Filtrer » (CTA principal du formulaire de recherche) est décalé vers le haut par rapport aux champs Recherche / Catégorie / Quartier sur écran large. Le bas du bouton ne tombe pas sur la même ligne que le bas des champs, ce qui donne une impression de finition bâclée.

## What Changes

- Aligner le bas du bouton « Filtrer » sur le bas des champs du formulaire de filtres (affichage ≥ 768 px).
- Aucun changement de comportement, de libellé ni de disposition mobile (en mobile, les éléments sont empilés et le bouton reste sous les champs).

Cause identifiée : la grille `.filters` aligne déjà ses colonnes en bas (`align-items: end`). Mais le formulaire porte `role="search"`, et Pico CSS retire la marge basse des `input`/`select` dans ce contexte, tandis que le bouton (`type="submit"`) garde la marge basse par défaut de Pico (`margin-bottom: var(--pico-spacing)`, soit 1rem). Le bouton est donc remonté d'environ 16 px.

## Capabilities

### New Capabilities

_Aucune._

### Modified Capabilities

_Aucune — correction purement visuelle, aucune exigence de spec ne change (`skip_specs: true`)._

## Impact

- `static/css/site.css` : une règle ciblant le bouton dans `.filters` pour annuler sa marge basse.
- Aucun template, aucune vue, aucune dépendance touchés.
