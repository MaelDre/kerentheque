## Why

Un visiteur qui arrive sur Kerentheque tombe directement sur le catalogue, sans explication sur l'esprit du projet, son fonctionnement ni les personnes qui le portent. Avant d'ouvrir l'application à des testeurs, il faut une page de présentation qui inspire confiance et explique la démarche.

## What Changes

- Nouvelle page statique « Le projet », accessible à l'adresse `/le-projet/` à tout visiteur, connecté ou non. Son contenu suit le plan : Pourquoi ? / Comment ça marche ? / Qui sommes-nous ? / Les prochaines étapes.
- Nouvelle entrée « Le projet » dans le menu de l'en-tête, présente que le visiteur soit connecté ou non, en style de lien simple.
- Nouveau lien « Le projet » dans le pied de page, à côté des mentions légales et de la page de confidentialité.
- Nouveau bandeau léger et permanent sur la page d'accueil (catalogue), qui met en avant le projet et propose un bouton secondaire menant à la page de présentation. Le bandeau ne remplace pas « Filtrer » comme action principale de l'accueil.

## Capabilities

### New Capabilities
- `project-presentation` : page de présentation du projet, accès à cette page depuis le menu et le pied de page, et bandeau de mise en avant sur l'accueil.

### Modified Capabilities
<!-- Aucune : le bandeau respecte les exigences existantes de ui-foundation (hiérarchie des actions, cibles tactiles) sans les modifier. -->

## Impact

- `config/urls.py` : nouvelle route `/le-projet/`.
- `templates/project.html` : nouveau gabarit.
- `templates/base.html` : entrée de menu et lien de pied de page.
- `items/templates/items/catalog.html` : bandeau.
- `static/css/site.css` : style du bandeau.
- Aucune nouvelle dépendance, aucune migration.
