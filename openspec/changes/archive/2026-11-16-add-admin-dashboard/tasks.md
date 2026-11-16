## 1. Calcul des indicateurs

- [x] 1.1 Ajouter `platform_stats()` dans `moderation/services.py` (objets non supprimés, membres actifs au profil complet, demandes totales, demandes acceptées), avec un commentaire qui renvoie à `User.is_profile_complete`
- [x] 1.2 Tests unitaires de `platform_stats()` : objet supprimé exclu, objet d'un compte suspendu inclus, comptes au profil incomplet, suspendu ou supprimé exclus, une demande par statut (4 au total, 1 acceptée)

## 2. Affichage dans l'administration

- [x] 2.1 Créer la balise d'inclusion `admin_dashboard` dans `moderation/templatetags/` : ne rend rien si `request.user` n'est pas superuser
- [x] 2.2 Créer le fragment `moderation/templates/moderation/admin_dashboard.html` : quatre cartes (valeur + libellé), styles basés sur les variables CSS de l'admin
- [x] 2.3 Créer `templates/admin/kerentheque_index.html`, qui étend `admin/index.html` et insère `{% admin_dashboard %}` avant `{{ block.super }}`
- [x] 2.4 Déclarer `admin.site.index_template` dans `config/urls.py`

## 3. Tests d'accès et vérification

- [x] 3.1 Test : un superuser voit les quatre libellés et les bonnes valeurs sur `admin:index`, et la liste des modules reste présente
- [x] 3.2 Test : un `is_staff` non superuser accède à `admin:index` sans voir les indicateurs
- [x] 3.3 Lancer toute la suite de tests et vérifier visuellement l'accueil de l'admin en local (thème clair et sombre, largeur mobile)
