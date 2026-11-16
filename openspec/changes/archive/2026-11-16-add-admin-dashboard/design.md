## Context

L'administration repose sur le `admin.site` par défaut de Django. `config/urls.py` le personnalise déjà (`site_header`, `site_title`). Les templates du projet se trouvent dans `templates/` (`DIRS`), et les applications ont `APP_DIRS` activé. Les définitions métier dont on a besoin existent déjà :
- `Item.objects.not_deleted()` ;
- `User.is_profile_complete` (pseudo, quartier, conditions acceptées). C'est une propriété Python, donc inutilisable dans une requête SQL ;
- `ContactRequest.Status.ACCEPTED`.

## Goals / Non-Goals

**Goals:**
- Afficher les quatre indicateurs sur l'accueil de `/admin/`, uniquement pour les super-administrateurs (`is_superuser`).
- Garder le calcul dans une fonction testable, indépendante de l'affichage, pour pouvoir la réutiliser plus tard (page dédiée, graphiques).

**Non-Goals:**
- Historique, évolution dans le temps, graphiques.
- Page hors de l'admin Django ou habillée avec le design system du site.
- Mise en cache des compteurs : les volumes de l'alpha rendent quatre `COUNT` négligeables.

## Decisions

### 1. Étendre l'accueil de l'admin plutôt que créer une page dédiée
Les actions de modération sont déjà dans `/admin/`, qui gère l'authentification et le contrôle d'accès. Y ajouter les indicateurs ne demande qu'un template et aucune nouvelle URL à sécuriser.
*Alternative écartée :* une page `/pilotage/` sur le site, plus soignée, mais qui oblige à recoder le contrôle d'accès et à maintenir deux interfaces.

### 2. Déclarer un template d'accueil via `admin.site.index_template`
On ajoute `admin.site.index_template = "admin/kerentheque_index.html"` dans `config/urls.py`, à côté de `site_header`. Ce template étend `admin/index.html` et insère les indicateurs avant `{{ block.super }}` dans le bloc `content`.
*Alternatives écartées :*
- Surcharger `templates/admin/index.html` sous le même nom : ça fonctionne, mais l'auto-extension d'un template homonyme est moins explicite.
- Sous-classer `AdminSite` : il faudrait réenregistrer tous les `ModelAdmin`, ce qui est disproportionné.

### 3. Fournir les données par une balise de template d'inclusion
Une balise `{% admin_dashboard %}` dans `moderation/templatetags/` lit `request.user` dans le contexte. Si l'utilisateur n'est pas superuser, elle ne rend rien. Sinon, elle appelle le service et rend le fragment `moderation/admin_dashboard.html`. Le contrôle `is_superuser` se fait ainsi côté serveur, au même endroit que le calcul : un non-superuser ne déclenche même pas les requêtes.
*Alternative écartée :* surcharger `admin.site.index` pour injecter un `extra_context`. C'est possible, mais il faudrait remplacer une méthode de l'instance globale, ce qui est moins lisible.

### 4. Calcul dans `moderation/services.py`
Une fonction `platform_stats()` renvoie un dictionnaire avec les quatre valeurs :
- objets : `Item.objects.not_deleted().count()` ;
- membres : `User.objects.filter(is_active=True, deleted_at__isnull=True, pseudo__isnull=False, neighborhood__isnull=False, terms_accepted_at__isnull=False).count()`. C'est la traduction en SQL de `is_profile_complete`. Un commentaire renverra à cette propriété pour qu'on pense à garder les deux alignées ;
- demandes : `ContactRequest.objects.count()` ;
- acceptées : `ContactRequest.objects.filter(status=ACCEPTED).count()`.

### 5. Présentation
Quatre cartes en ligne (grille CSS en ligne dans le fragment, qui passe sur plusieurs lignes sur petit écran), chacune avec une grande valeur et un libellé. Le style s'appuie sur les variables CSS de l'admin Django (`--body-fg`, `--hairline-color`…) pour rester lisible en thème clair comme en thème sombre.

## Risks / Trade-offs

- [La définition « profil complet » est dupliquée entre la propriété Python et le filtre SQL] → Commentaire croisé, plus un test qui crée un profil incomplet pour chaque critère manquant.
- [Le template de l'admin Django peut évoluer d'une version à l'autre] → On ne s'appuie que sur le bloc `content` et `block.super`, qui sont stables. Un test vérifie que la liste des modules reste affichée.
- [Le libellé « Mises en relation acceptées » peut surprendre] → C'est un choix volontaire pour ne pas laisser croire qu'il s'agit de prêts effectifs.
