## 1. Correction CSS

- [x] 1.1 Dans `static/css/site.css`, annuler la marge basse du bouton du formulaire de filtres (`.filters button { margin-bottom: 0; }`, spécificité supérieure à la règle Pico `[type=submit]`)

## 2. Vérification

- [x] 2.1 Sur le catalogue en largeur ≥ 768 px, vérifier que le bas du bouton « Filtrer » est aligné avec le bas des champs Recherche / Catégorie / Quartier, et que les hauteurs sont identiques (44 px minimum)
- [x] 2.2 En largeur 360 px, vérifier que le formulaire empilé reste correct (pas de défilement horizontal, espacement acceptable sous le bouton)
- [x] 2.3 Lancer la suite de tests existante pour s'assurer qu'aucune régression n'est introduite
