## 1. Logique de palier

- [x] 1.1 Créer `items/milestones.py` : constante `MILESTONES`, dataclass immuable (`target`, `percent`, `missing`, `is_close`) et fonction `milestone_progress(count)` qui renvoie `None` à partir de 1000
- [x] 1.2 Tests unitaires de `milestone_progress` : 0 → 25 / 0 % / 25 manquants ; 24 → 1 manquant ; 25 → 50 / 50 % ; 87 → 100 / 87 % / 13 / proche ; 120 → 200 / 60 % / pas proche ; 999 → 1000 ; 1000 et 1500 → `None`

## 2. Vue et template

- [x] 2.1 Dans `items.views.catalog`, ajouter `item_count` (`Item.objects.available().count()`, indépendant des filtres) et `milestone` au contexte
- [x] 2.2 Créer le fragment `items/templates/items/home_stats.html` : compteur (singulier pour 0 et 1, nombres en `floatformat:"g"`), bloc palier (titre, pourcentage, pastille « Bientôt atteint », `<progress>` avec `aria-label`, bornes 0 / palier, objets manquants accordés), et, sans palier, phrase d'invitation seule ; bouton « Ajouter un objet » vers `items:create` (connecté) ou `accounts:login` (anonyme)
- [x] 2.3 Inclure le fragment dans `catalog.html`, entre le bandeau projet et les filtres ; passer le bouton « Filtrer » en `class="secondary"`

## 3. Styles

- [x] 3.1 Ajouter dans `static/css/site.css` les styles des deux blocs à partir des tokens uniquement : cartes `surface-raised` + filet `border` + `radius-lg`, chiffre en `font-display` `brand`, `<progress>` unie `brand`, pastille `accent` / `ink` en `radius-pill`, bouton non pleine largeur ; vérifier le rendu à largeur mobile

## 4. Tests de la page et vérification

- [x] 4.1 Tests de vue : le compteur exclut les objets supprimés et ceux des comptes suspendus ; il ne change pas avec une recherche ou un filtre ; « 0 objet disponible » et « 1 objet disponible » au singulier ; la mention « Bientôt atteint » apparaît à 87 objets et pas à 120
- [x] 4.2 Tests du bouton : un membre connecté a un lien vers `items:create`, un visiteur anonyme a un lien vers `accounts:login`
- [x] 4.3 Test au-delà du dernier palier : avec 1000 objets, pas de `<progress>` ni de « Prochain palier », mais le bouton est présent (palier forcé par patch de `MILESTONES` si créer 1000 objets ralentit trop la suite)
- [x] 4.4 Lancer toute la suite de tests et vérifier visuellement l'accueil en local (connecté / anonyme, mobile et desktop, cas 0, 87, ≥ 1000)
