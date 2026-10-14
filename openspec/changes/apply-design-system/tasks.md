## 1. Branchement du design system

- [x] 1.1 Commiter le dossier `design-system/` (tokens, polices, DESIGN.md) tel que fourni
- [x] 1.2 Ajouter `("design-system", BASE_DIR / "design-system")` à `STATICFILES_DIRS` dans `config/settings.py`, puis vérifier avec `collectstatic` que `staticfiles/design-system/fonts/` est créé et que les `url()` de `tokens.css` sont réécrites vers les fichiers hachés
- [x] 1.3 Dans `templates/base.html` : charger `design-system/tokens.css` avant Pico, ajouter `data-theme="light"` sur `<html>` et passer `color-scheme` à `light`

## 2. Thème Pico

- [x] 2.1 Créer `static/css/theme.css`, chargé après Pico, qui associe les tokens aux variables `--pico-*` sous `:root[data-theme="light"]` (voir design.md §5)
- [x] 2.2 Appliquer `--font-display` aux titres et supprimer les ombres de Pico (cartes, boutons, champs)
- [x] 2.3 Remplacer le focus de Pico par l'anneau du DS : 2px `brand`, décalé de 2px, sur tous les éléments interactifs
- [x] 2.4 Garantir une hauteur minimale de 44px pour les boutons, `[role=button]`, champs, selects, `summary` et entrées du menu « Mon compte », dont le bouton « Se déconnecter »
- [x] 2.5 Garantir un texte à 16px minimum dans les champs de saisie
- [x] 2.6 Définir les variantes de boutons : `.secondary` (et `.outline` aligné dessus), `.danger` et `.secondary.danger` (voir design.md §6), avec un survol dérivé de `brand` par `color-mix()`
- [x] 2.7 Vérifier que `theme.css` reste sous environ 150 lignes. Sinon, s'arrêter et en parler (garde-fou de design.md §1)

## 3. Composants propres à Kerentheque

- [x] 3.1 Réécrire `static/css/site.css` avec les tokens uniquement : supprimer `--kt-success`, `--kt-muted` et toutes les couleurs, tailles et rayons en dur
- [x] 3.2 Cartes d'objets : fond `surface-raised`, filet `border`, `radius-lg`, padding `space-4`, nom en style `subtitle`
- [x] 3.3 Statuts de demande en pastilles (`radius-pill`) avec les fonds `accent`, `brand-tint` et `surface-sunken` (voir design.md §7)
- [x] 3.4 Messages flash et erreurs de champ : couleurs du DS, le libellé textuel reste toujours présent
- [x] 3.5 Zone de filtres du catalogue sur fond `surface-sunken` ; métadonnées (`.meta`) en `ink-muted`

## 4. Hiérarchie des actions dans les templates

- [x] 4.1 `base.html` : le bouton « Se connecter » de l'en-tête passe en secondaire
- [x] 4.2 Formulaires avec annulation (`items/form.html`, `moderation/report.html`, `feedback/send.html`) : « Annuler » passe de `.outline` à `.secondary`
- [x] 4.3 Confirmations de suppression (`items/delete.html`, `accounts/delete_account.html`) : bouton de suppression en `.danger`, « Annuler » en `.secondary`
- [x] 4.4 `items/detail.html` : « Supprimer » en `.secondary.danger`
- [x] 4.5 `contacts/received.html` : « Refuser » en `.secondary`
- [x] 4.6 Vérifier qu'il ne reste aucune classe `.outline` ni aucune couleur en dur (`grep` sur les templates et `static/css/site.css`)

## 5. Tests et recette

- [x] 5.1 Ajouter un test Django qui vérifie qu'une page rendue charge `design-system/tokens.css` et porte `data-theme="light"`
- [x] 5.2 Lancer la suite de tests complète et vérifier qu'elle passe
- [x] 5.3 Recette visuelle sur le catalogue, le détail d'un objet, le formulaire d'objet, les demandes reçues et envoyées, la connexion, le profil et la page 404 : polices et couleurs du DS, au plus une action principale par page ou par élément de liste
- [x] 5.4 Recette d'accessibilité : affichage en clair avec l'OS en mode sombre, parcours complet au clavier avec focus visible, vue mobile (cibles de 44px, champs sans zoom), contrastes vérifiés dans l'inspecteur du navigateur
- [ ] 5.5 Déployer sur Railway et vérifier que les polices se chargent en production (aucune erreur 404 sur `fonts/` dans l'onglet Réseau)
