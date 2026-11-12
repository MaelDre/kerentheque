## 1. Correction CSS

- [x] 1.1 Dans `static/css/site.css`, remplacer `gap: 0 var(--space-4)` par `gap: var(--space-3) var(--space-4)` sur `.filters`

## 2. Vérification

- [x] 2.1 En largeur 360 px, vérifier que chaque libellé est visiblement séparé du champ au-dessus et que le bouton « Filtrer » ne touche plus le sélecteur « Quartier », sans défilement horizontal
- [x] 2.2 En largeur ≥ 768 px, vérifier que la ligne de filtres est inchangée (bouton toujours aligné en bas avec les champs)
- [x] 2.3 Lancer la suite de tests existante pour s'assurer qu'aucune régression n'est introduite
