Système de design minimal pour une application de prêt d'objets entre habitants d'une commune. Il vise la confiance et la lisibilité : fond chaud, texte très contrasté, un seul vert pour les actions. Nom de travail « Prêt commun » : à remplacer par celui de l'application.

## Principes de rédaction

- Tutoyer ou vouvoyer, mais un seul registre dans toute l'application. Par défaut : vouvoiement, ton simple et chaleureux, comme un voisin poli.
- Verbes d'action à l'infinitif sur les boutons : « Emprunter », « Proposer un objet », « Confirmer le retrait ».
- Écrire en phrase normale, majuscule initiale seulement. Pas de capitales intégrales, pas d'emoji décoratif.
- Dire qui, quoi, quand, où : « Prêté par Camille, disponible du 12 au 14 octobre ».
- Un message d'erreur dit ce qui s'est passé et comment s'en sortir : « Cet objet est déjà réservé ces jours-là. Choisissez d'autres dates. »

## Couleur

- Fond de page : `surface`. Cartes et champs : `surface-raised`. Zones en retrait : `surface-sunken`.
- Texte : `ink` par défaut, `ink-muted` pour l'aide et les métadonnées.
- L'action principale d'un écran est un bouton `brand` avec du texte `on-brand`. Une seule par écran ; les autres actions sont des boutons secondaires (fond `surface-raised`, bordure `border-strong`, texte `ink`).
- `brand-tint` met en avant un contenu (objet disponible, information). `accent` ne s'emploie qu'en fond de pastille avec du texte `ink`, jamais en texte.
- `danger` signale une erreur ou une suppression, toujours avec un mot ou une icône : l'état ne doit jamais reposer sur la couleur seule.
- Bordures : `border` pour séparer des cartes, `border-strong` pour tout contrôle interactif (3:1 minimum).
- Focus clavier : anneau plein de 2px en `brand`, décalé de 2px, visible sur toutes les surfaces.

## Typographie

- Deux familles. `display` (Outfit, sans géométrique aux formes rondes et directes) pour les titres : styles `display` (700) et `title` (600), jamais en capitales. `sans` (Atkinson Hyperlegible Next, conçue pour la lisibilité des personnes malvoyantes) pour tout le reste.
- Un `display` par écran, `title` pour les sections, `subtitle` pour le nom d'un objet, `body` pour le texte courant.
- `label` pour les boutons et libellés de champs, `small` pour les métadonnées, `caption` seulement pour du secondaire.
- Texte courant jamais sous 16px dans les champs de saisie (évite le zoom automatique sur mobile).
- Les deux polices sont sous licence SIL Open Font License : libres pour un usage commercial ou public, à servir depuis vos propres fichiers (`fonts/`).

## Espacement et formes

- Échelle `space-1` à `space-8`, multiples de 4px. Marge latérale mobile : `space-4`.
- Boutons et champs : `radius-md`, padding vertical `space-3`. Cartes d'objets : `radius-lg`, padding `space-4`. Filtres et étiquettes : `radius-pill`.
- Séparer par des filets `border` plutôt que par des ombres ; pas de dégradés.

## Accessibilité

- Cibles tactiles de 44px minimum de hauteur.
- Tout texte respecte 4,5:1 sur le fond indiqué dans la note de son token.
- Toute image d'objet a un texte alternatif (« Perceuse sans fil bleue »).

## Logo et icônes

Aucun logo ni jeu d'icônes n'est encore fourni : afficher le nom de l'application en `title`, et utiliser un seul jeu d'icônes au trait (même épaisseur, couleur `ink` ou `brand`) lorsqu'il sera choisi.

## Utilisation dans le code

- Charger `tokens.css` une fois au plus haut niveau de l'application ; il déclare les polices (`fonts/`) et toutes les variables CSS (`var(--brand)`, `var(--space-4)`, `var(--radius-lg)`, `var(--font-display)`…).
- Ne jamais écrire une couleur, une taille ou un rayon en dur : utiliser le token correspondant. Les classes `.display`, `.title`, `.subtitle`, `.body`, `.label`, `.small`, `.caption` appliquent les styles de texte.
- `tokens.json` contient les mêmes valeurs avec leur note d'usage, pour un outil ou une configuration (Tailwind, thème d'un framework…).
