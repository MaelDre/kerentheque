## 1. Gabarits

- [x] 1.1 Dans `items/templates/items/item_card.html`, n'afficher le pseudo du propriétaire que si `user.is_authenticated` (catégorie et quartier restent affichés pour tous)
- [x] 1.2 Dans l'en-tête de `items/templates/items/detail.html`, n'afficher « Prêté par <pseudo> » que si `user.is_authenticated`
- [x] 1.3 Dans `items/templates/items/detail.html`, remplacer le libellé du bouton pour les visiteurs par « Se connecter pour contacter le prêteur »
- [x] 1.4 Mettre à jour le texte de `items/templates/items/form.html` : l'objet est visible par tous avec votre quartier, et votre pseudo n'est montré qu'aux membres connectés
- [x] 1.5 Mettre à jour `accounts/templates/accounts/privacy.html` : quartier affiché publiquement avec vos objets, pseudo visible uniquement par les membres connectés

## 2. Tests

- [x] 2.1 Adapter `test_anonymous_sees_catalog` : le catalogue anonyme contient le nom de l'objet et le quartier, mais pas le pseudo du propriétaire
- [x] 2.2 Ajouter un test : un membre connecté voit le pseudo et le quartier du propriétaire dans le catalogue
- [x] 2.3 Étendre `test_detail_for_anonymous_invites_login` : la fiche anonyme invite à se connecter et ne contient pas le pseudo du propriétaire
- [x] 2.4 Ajouter un test : un membre connecté non propriétaire voit le pseudo du propriétaire sur la fiche
- [x] 2.5 Lancer toute la suite de tests et vérifier qu'elle passe
