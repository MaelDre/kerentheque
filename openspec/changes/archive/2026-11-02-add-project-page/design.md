## Context

Les pages statiques existantes (mentions légales, confidentialité) sont servies par un `TemplateView` déclaré dans `accounts/urls.py`, sans vue Python. L'en-tête et le pied de page sont définis une seule fois dans `templates/base.html`. L'accueil est `items/templates/items/catalog.html`, dont « Filtrer » est l'action principale. Le style suit le design system (`design-system/DESIGN.md`) appliqué via `theme.css` et `site.css`.

## Goals / Non-Goals

**Goals:**
- Ajouter la page et ses accès sans nouvelle dépendance ni nouvelle app Django.
- Fournir un premier contenu rédigé, facile à modifier sans toucher au code Python.

**Non-Goals:**
- Bandeau masquable par l'utilisateur (cookie, JavaScript) : il est permanent pour l'instant.
- Contenu administrable depuis l'admin Django.
- Illustrations ou logo sur la page.

## Decisions

**Route déclarée dans `config/urls.py`, gabarit `templates/project.html`.**
La page ne relève d'aucune app métier (`accounts`, `items`…). La déclarer dans `accounts/urls.py`, comme les pages légales, la rangerait sous un nom de route trompeur (`accounts:project`) et sous le préfixe `/compte/`. Une app dédiée `pages` serait surdimensionnée pour une seule page. La route est nommée `project` (sans espace de noms) : `{% url 'project' %}`.

**`TemplateView` sans vue Python.**
Ce modèle est déjà utilisé pour les pages légales. Le contenu vit entièrement dans le gabarit HTML, qu'on modifie sans toucher au Python.

**Entrée de menu dans la partie droite de l'en-tête, avant les liens propres à chaque état.**
L'entrée est placée une seule fois, avant le bloc `{% if user.is_authenticated %}`. Elle apparaît ainsi dans les deux cas, sans duplication. C'est un lien simple, sans `role="button"`, conformément à la règle « la navigation n'utilise pas le style principal ».

**Bandeau : bloc `brand-tint` sur une ligne, placé entre le titre et les filtres.**
- Le fond `brand-tint` est la couleur que le design system réserve à « mettre en avant une information ». Pas de bordure épaisse, pas d'image : seulement un padding réduit (`space-3`/`space-4`) et une seule phrase.
- Mise en page en flex : le texte à gauche, le bouton à droite. Le bloc passe sur deux lignes sur mobile (`flex-wrap`).
- Le bouton est un lien `role="button" class="secondary"`, le style secondaire déjà défini, avec une cible tactile de 44px héritée du thème.
- Alternative écartée : placer le bandeau au-dessus du titre. Il passerait alors avant le contenu principal de l'accueil et prendrait trop d'importance visuelle.

**Tests dans un nouveau `config/tests.py`.**
Le module `config` est un paquet Python, donc le lanceur de tests Django le découvre. Les tests vérifient : statut 200 sans connexion, présence des 4 titres, présence des liens dans l'en-tête et le pied de page (connecté et non connecté), présence du bandeau sur l'accueil et son absence ailleurs.

**Contenu initial de la page** (rédigé au vouvoiement, ton simple, conformément au design system) :

- *Pourquoi ?* Beaucoup d'objets du quotidien (perceuse, escabeau, appareil à raclette, tente) servent quelques heures par an et dorment le reste du temps dans un placard. Les prêter entre voisins évite des achats inutiles, libère de la place, réduit les déchets et crée du lien dans le quartier.
- *Comment ça marche ?* Trois étapes : 1) vous listez les objets que vous acceptez de prêter, en public (visibles dans le catalogue avec votre nom) ou en privé ; 2) un voisin trouve un objet dans le catalogue et vous envoie une demande ; 3) si vous acceptez, vos coordonnées sont échangées et le prêt s'organise directement entre vous, hors de l'application.
- *Qui sommes-nous ?* Texte à trous, marqué `{# TEXTE PROVISOIRE #}` comme les mentions légales : « Kerentheque est un projet [bénévole / associatif] porté par [prénom(s)], habitant(s) de [commune]. » Le contenu n'invente pas d'identité : c'est au porteur du projet de le compléter.
- *Les prochaines étapes :* phase de test avec un premier groupe d'habitants ; amélioration à partir des retours (lien vers « Nous contacter » pour les membres connectés) ; ouverture plus large dans la commune. La formulation reste générale et ne promet aucune date.

## Risks / Trade-offs

- [Le menu s'alourdit sur mobile avec une entrée de plus] → La navigation passe déjà à la ligne (`flex-wrap`) ; le libellé est court. À vérifier visuellement à 360px de large.
- [Le bandeau permanent finit par lasser les membres réguliers] → Choix assumé pour l'instant. Le rendre conditionnel (visiteurs non connectés seulement) ne demandera qu'une condition dans le gabarit.
- [La section « Qui sommes-nous ? » est publiée avec des crochets] → Elle est marquée comme texte provisoire et doit être complétée avant l'arrivée d'un testeur, comme les mentions légales.

## Open Questions

- Le texte définitif de « Qui sommes-nous ? » : nom(s), commune, statut (bénévole, association). Il se complète dans le gabarit sans impact sur la spec ni sur les tâches.
