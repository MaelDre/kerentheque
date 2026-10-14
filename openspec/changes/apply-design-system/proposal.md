## Why

Kerentheque utilise aujourd'hui le thème par défaut de Pico CSS, avec quelques couleurs écrites en dur. L'application n'a donc pas d'identité visuelle propre, et plusieurs règles d'accessibilité ne sont pas garanties. Un design system existe désormais (`design-system/` : tokens, polices, règles d'usage). L'appliquer avant d'ouvrir l'alpha à d'autres testeurs donne une interface cohérente, chaleureuse et lisible, qui inspire confiance aux habitants.

## What Changes

- Charger les tokens et les polices du design system (Outfit pour les titres, Atkinson Hyperlegible Next pour le texte) sur toutes les pages.
- Re-thémer Pico CSS en associant ses variables aux tokens : fond, texte, bordures, couleur principale, rayons et polices. Pico reste en place.
- **BREAKING** : retirer le mode sombre automatique. L'application s'affiche toujours en thème clair, le seul défini par le design system.
- Hiérarchiser les actions : une seule action principale (`brand`) par écran, les autres en boutons secondaires, et les suppressions en `danger`.
- Afficher les statuts des demandes de contact sous forme de pastilles portant le libellé du statut, au lieu d'une couleur de texte.
- Garantir les exigences d'accessibilité du design system : cibles tactiles de 44px minimum, anneau de focus visible, texte des champs à 16px minimum, contrastes, et aucun état signalé par la seule couleur.
- Nettoyer `static/css/site.css` : plus aucune couleur, taille ou rayon en dur, seulement des tokens.

Hors périmètre :
- la microcopie et les principes de rédaction du design system, prévus dans un change séparé ;
- la conversion des polices en WOFF2, qui demanderait une nouvelle dépendance ;
- le logo et les icônes, que le design system ne fournit pas encore ;
- les textes alternatifs d'images, puisque l'application n'affiche pas encore d'image d'objet.

## Capabilities

### New Capabilities
- `ui-foundation` : socle commun de l'interface, à savoir l'identité visuelle appliquée à toutes les pages et les exigences d'accessibilité vérifiables (cibles tactiles, focus, taille de saisie, contrastes, états non portés par la seule couleur, hiérarchie des actions).

### Modified Capabilities
_Aucune._ Les écrans existants changent d'apparence, mais pas de comportement fonctionnel.

## Impact

- **Templates** : `templates/base.html` (feuilles de style, thème clair forcé) et les templates contenant des boutons ou des statuts (`items/`, `contacts/`, `accounts/`, `moderation/`, `feedback/`, pages 404/500).
- **CSS** : nouvelle feuille de thème qui associe les tokens aux variables de Pico, et `static/css/site.css` réécrit avec les tokens.
- **Configuration** : `design-system/` ajouté à `STATICFILES_DIRS` dans `config/settings.py`. La source du design system reste unique, et `collectstatic` (build Docker) l'embarque automatiquement.
- **Poids des pages** : environ 225 Ko de polices TTF au premier chargement, mis en cache ensuite.
- **Dépendances** : aucune nouvelle.
