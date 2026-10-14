## Context

Le front repose sur Pico CSS v2 (`static/css/pico.min.css`), un framework « sans classes » qui stylise directement le HTML sémantique, complété par `static/css/site.css` (environ 60 lignes, avec des couleurs en dur). Les 22 templates utilisent surtout des éléments natifs (`<article>`, `<nav>`, `<details class="dropdown">`, formulaires) et quelques variantes de Pico (`role="button"`, `.outline`, `.secondary`).

Le design system (`design-system/`) fournit :
- `tokens.css`, qui déclare les polices avec des chemins relatifs (`fonts/…`), les variables CSS et les classes de texte ;
- `tokens.json` (mêmes valeurs, avec leurs notes d'usage) ;
- `DESIGN.md` (règles d'usage).

Il définit des tokens et quelques règles de composants (boutons, focus, cartes, pastilles). Il ne dit rien des menus, des selects ni de la pagination.

Les fichiers statiques sont servis par WhiteNoise, avec `CompressedManifestStaticFilesStorage` en production. `collectstatic` tourne au build Docker.

## Goals / Non-Goals

**Goals :**
- Garder `design-system/` comme source unique : aucune valeur du DS recopiée à la main dans le code de l'application.
- Limiter les retouches de templates à ce qu'exigent la hiérarchie des actions et les statuts.
- Garder la surcharge de Pico petite et lisible.

**Non-Goals :**
- Créer une bibliothèque de composants ou des templates partiels pour les boutons.
- Ajouter un outil de build CSS (Sass, PostCSS, Tailwind).
- Mettre en place des tests visuels automatisés.

## Decisions

### 1. Garder Pico et le re-thémer plutôt que le retirer

Le DS définit des tokens, pas un jeu complet de composants. Pico continue de styliser tout ce que le DS ne décrit pas (menu déroulant, selects, cases à cocher, mise en page responsive), et ces éléments prennent automatiquement les couleurs et polices du DS via les variables `--pico-*`.

*Alternative écartée :* retirer Pico et écrire une feuille complète. On aurait 100 % de fidélité au DS, mais il faudrait inventer le style de chaque élément non décrit et l'écrire à la main pour chaque nouvel élément HTML. C'est trop coûteux pour une alpha.

*Garde-fou :* si `theme.css` dépasse environ 150 lignes, ou si l'implémentation passe son temps à corriger des comportements de Pico, il faut s'arrêter et envisager le retrait de Pico dans un change dédié. Les tokens restant la source de vérité, ce passage n'invaliderait rien.

### 2. Servir `design-system/` tel quel via `STATICFILES_DIRS`

On ajoute `BASE_DIR / "design-system"` à `STATICFILES_DIRS` avec un préfixe : `("design-system", BASE_DIR / "design-system")`. Les fichiers sont alors servis sous `static/design-system/tokens.css` et `static/design-system/fonts/…`. Le chemin relatif `fonts/` de `tokens.css` reste valide, et le stockage « manifest » de WhiteNoise réécrit les `url()` vers les noms hachés.

*Alternative écartée :* copier `tokens.css` et `fonts/` dans `static/`. On aurait deux copies à synchroniser à chaque évolution du DS.

*Conséquence acceptée :* `DESIGN.md` et `tokens.json` sont aussi publiés en statique. Ils ne contiennent rien de sensible.

### 3. Ordre et rôle des feuilles de style

```
base.html
  1. design-system/tokens.css   tokens, @font-face, classes de texte
  2. css/pico.min.css           base de Pico
  3. css/theme.css              tokens → variables --pico-*, surcharges de Pico
  4. css/site.css               composants propres à Kerentheque (tokens seulement)
```

- `theme.css` (nouveau) contient uniquement le pont entre le DS et Pico, plus les surcharges globales : pas d'ombres, anneau de focus, hauteur minimale de 44px, champs à 16px, rayons. On peut le relire d'un coup d'œil pour voir où l'on contredit Pico.
- `site.css` garde les composants métier (cartes d'objets, pastilles de statut, messages, filtres, pagination), réécrits avec les tokens.

### 4. Forcer le thème clair

On pose `data-theme="light"` sur `<html>` et on remplace `color-scheme: light dark` par `light`. Pico déclare ses variables claires sur `[data-theme=light], :root:not([data-theme=dark])`. Les surcharges de `theme.css` utilisent donc le sélecteur `:root[data-theme="light"]`, de spécificité au moins égale, et la feuille est chargée après Pico pour que ses valeurs l'emportent sans `!important`.

### 5. Correspondance entre les tokens et Pico (principe)

| Pico | Token |
|---|---|
| `--pico-background-color` | `--surface` |
| `--pico-color`, titres | `--ink` |
| `--pico-muted-color` | `--ink-muted` |
| `--pico-primary*`, `--pico-primary-background` | `--brand` / `--on-brand` |
| `--pico-card-background-color`, `--pico-form-element-background-color` | `--surface-raised` |
| `--pico-muted-border-color`, `--pico-card-border-color` | `--border` |
| `--pico-form-element-border-color` | `--border-strong` |
| `--pico-del-color`, `--pico-form-element-invalid-border-color` | `--danger` |
| `--pico-border-radius` | `--radius-md` |
| `--pico-font-family` | `--font-sans` |
| `--pico-box-shadow`, `--pico-card-box-shadow`, `--pico-button-box-shadow` | `none` |

Les titres `h1`–`h3` reçoivent `--font-display` dans `theme.css`. Les états de survol de `brand` (une teinte plus foncée) ne sont pas définis par le DS. On utilisera `color-mix()` sur `--brand` plutôt qu'une nouvelle couleur en dur, et le DS pourra être complété ensuite.

### 6. Hiérarchie des boutons

Le style principal reste le bouton Pico par défaut (fond `brand`). Les variantes de Pico sont remappées pour coller au vocabulaire du DS, sans introduire de nouvelles classes :

| Usage DS | Balisage | Rendu |
|---|---|---|
| Principal | `<button>`, `role="button"` | fond `brand`, texte `on-brand` |
| Secondaire | `.secondary` | fond `surface-raised`, bordure `border-strong`, texte `ink` |
| Danger (confirmation de suppression) | `.danger` | fond `danger`, texte `on-danger` |
| Danger (lien vers la suppression) | `.secondary.danger` | secondaire avec texte et bordure `danger` |

Pour éviter de maintenir trois apparences proches, `.outline` est aligné visuellement sur `.secondary`, puis les templates sont harmonisés vers `.secondary`. La classe `.danger` est la seule nouvelle classe de bouton. Le bouton « Se connecter » de l'en-tête passe en secondaire, pour respecter la règle « une seule action principale ».

Écrans concernés : `items/detail.html` (Supprimer → secondaire danger), `items/delete.html` et `accounts/delete_account.html` (bouton de suppression → danger, Annuler → secondaire), `contacts/received.html` (Refuser → secondaire), les formulaires avec Annuler (`items/form.html`, `moderation/report.html`, `feedback/send.html`) et `base.html` (Se connecter).

### 7. Statuts en pastilles

`contacts/status.html` garde son balisage (`.status.status-<code>`). Seul le CSS change : fond en pastille (`radius-pill`), texte `ink`.

| Statut | Fond |
|---|---|
| `pending` | `accent` |
| `accepted` | `brand-tint` |
| `refused`, `cancelled` | `surface-sunken`, texte `ink-muted` |

Le libellé du statut est déjà affiché (`get_status_display`), ce qui satisfait l'exigence « jamais la couleur seule ».

### 8. Vérification

Les exigences de `ui-foundation` sont essentiellement visuelles. La vérification se fait par une recette manuelle documentée dans les tâches : navigateur en mode sombre, parcours au clavier, vue mobile dans les outils de développement, mesure des contrastes avec l'inspecteur. On ajoute un test Django léger qui vérifie que `base.html` référence `tokens.css` et porte `data-theme="light"`, pour éviter une régression silencieuse.

## Risks / Trade-offs

- **[Pico change ses sélecteurs ou ses variables dans une future version]** → Pico est vendorisé (fichier minifié commité) et ne bouge pas sans action explicite. Toutes les surcharges sont concentrées dans `theme.css`.
- **[Hauteur minimale de 44px trop large pour certains éléments, comme les liens du menu déroulant ou le bouton-lien de déconnexion]** → On cible explicitement les éléments interactifs (`button`, `[role=button]`, `input`, `select`, `summary`, entrées du menu) et pas les liens dans le texte courant.
- **[Polices TTF lourdes, environ 225 Ko]** → `font-display: swap` affiche le texte immédiatement avec la police de secours. WhiteNoise compresse et met en cache. La conversion en WOFF2 est notée comme sujet reporté.
- **[`color-mix()` pour le survol]** → Fonction CSS prise en charge par tous les navigateurs récents. Sur un navigateur ancien, le survol reste simplement de la couleur `brand`.
- **[Perte du mode sombre pour les utilisateurs qui en profitaient]** → Assumée (voir proposal). On pourra la réintroduire quand le DS définira un thème sombre.

## Migration Plan

Le déploiement suit le flux habituel (git push, build Docker, `collectstatic`). Aucune migration de données. En cas de problème, il suffit de revenir au commit précédent : le changement ne touche que des templates, du CSS et un réglage de `settings.py`.
