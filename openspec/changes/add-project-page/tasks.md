## 1. Page « Le projet »

- [x] 1.1 Ajouter la route `le-projet/` nommée `project` (`TemplateView`) dans `config/urls.py`
- [x] 1.2 Créer `templates/project.html` (étend `base.html`) avec les sections « Pourquoi ? », « Comment ça marche ? », « Qui sommes-nous ? » et « Les prochaines étapes », rédigées selon design.md ; marquer « Qui sommes-nous ? » comme texte provisoire

## 2. Accès depuis le menu et le pied de page

- [x] 2.1 Ajouter l'entrée « Le projet » (lien simple) dans la partie droite de l'en-tête de `templates/base.html`, avant le bloc connecté / non connecté
- [x] 2.2 Ajouter le lien « Le projet » dans le pied de page de `templates/base.html`, à côté de « Mentions légales » et « Confidentialité »

## 3. Bandeau sur l'accueil

- [x] 3.1 Ajouter le bandeau (une phrase et un bouton secondaire vers `/le-projet/`) dans `items/templates/items/catalog.html`, entre le titre et les filtres
- [x] 3.2 Styler le bandeau dans `static/css/site.css` avec les tokens (fond `brand-tint`, padding réduit, flex avec retour à la ligne sur mobile)

## 4. Tests et vérification

- [x] 4.1 Créer `config/tests.py` : la page renvoie 200 sans connexion et avec connexion, et contient les 4 titres dans l'ordre
- [x] 4.2 Tester la présence du lien « Le projet » dans l'en-tête et le pied de page, pour un visiteur connecté et un visiteur non connecté
- [x] 4.3 Tester la présence du bandeau et de son lien sur l'accueil, et son absence sur la page « Le projet » et sur le détail d'un objet
- [x] 4.4 Lancer toute la suite de tests et vérifier visuellement l'accueil et le menu à largeur mobile (360px) et sur ordinateur
