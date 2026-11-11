## Context

- Le site n'utilise aujourd'hui **aucun JavaScript** : templates Django rendus côté serveur et Pico CSS. `templates/base.html` n'expose que les blocs `title` et `content`, et aucune Content-Security-Policy n'est configurée.
- `accounts/services.py` → `delete_account()` anonymise déjà le compte (email, pseudo, téléphone, quartier) et vide les coordonnées recopiées dans `ContactRequest`. Il ne touche ni à `Item.description`, ni à `ContactRequest.message`, ni à `Report.reason`.
- `Item.search_text` est un champ dérivé, alimenté à partir du nom et de la description de l'objet.
- Le message d'une demande est aussi envoyé par email au propriétaire au moment de la demande (spec `contact-requests`). On ne peut pas rappeler cette copie.
- Les emails partent par SMTP Gmail. Le formulaire de retour (`feedback`) envoie les messages des membres dans la boîte de l'éditeur.

## Goals / Non-Goals

**Goals :**
- Des textes légaux exacts par rapport au comportement réel du code.
- Un email de contact inexploitable par une collecte automatique simple, mais accessible.

**Non-Goals :**
- Protéger d'autres adresses (l'adresse Gmail expéditrice reste visible dans les emails envoyés).
- Une protection contre un robot qui exécute JavaScript : on accepte cette limite.

## Decisions

### 1. Email assemblé en JavaScript, à partir de morceaux posés dans des attributs `data-`

Un fragment `templates/includes/protected_email.html` produit un élément du type `<a class="protected-email" data-user="mael.dreano" data-domain="pm.me">` accompagné d'un repli `mael.dreano [at] pm.me`. Un script `static/js/protected-email.js` (une dizaine de lignes, sans dépendance) remplace le repli par un vrai lien `mailto:`.

Le fragment prend l'utilisateur et le domaine en paramètres (`{% include ... with user="mael.dreano" domain="pm.me" %}`). Ainsi, l'adresse complète n'apparaît jamais d'un seul tenant, ni dans le HTML servi ni dans le dépôt Git.

*Pourquoi* : c'est la méthode la plus simple qui reste accessible (le repli est lisible sans JS et par les lecteurs d'écran) et qui ne demande ni dépendance ni formulaire à protéger.

*Alternatives écartées* :
- Forme « [at] » seule : les robots savent la décoder.
- Email en image : inaccessible et impossible à copier.
- Formulaire de contact : ouvre une nouvelle surface de spam, et le formulaire `feedback` existe déjà pour les membres.
- Base64 dans un attribut : n'apporte rien de plus que le découpage et rend le template moins lisible.

### 2. Script chargé par un nouveau bloc `scripts` dans `base.html`

On ajoute `{% block scripts %}{% endblock %}` juste avant `</body>`. Seules les deux pages légales le remplissent avec `<script src="{% static 'js/protected-email.js' %}" defer>`.

*Pourquoi* : le reste du site garde son fonctionnement sans JS, et un bloc dédié est le mécanisme standard de Django pour ajouter des ressources page par page. Pas de script inline : ça reste compatible avec une éventuelle future CSP.

### 3. Effacement des textes libres dans `delete_account()`, dans la transaction existante

On ajoute à la transaction :
- `description = ""` et recalcul de `search_text` pour les objets du membre ;
- `message = ""` sur les `ContactRequest` dont il est le demandeur.

*Pourquoi* : tout l'effacement reste au même endroit et se fait de façon atomique, comme aujourd'hui. On utilise un `update()` en masse si `search_text` peut être recalculé à partir du seul nom, sinon une boucle avec `save()` : à vérifier dans `items/models.py` au moment de l'implémentation. Comme les objets sont déjà retirés du catalogue, la recherche ne les remonte de toute façon pas.

*Conservés volontairement* : `Item.name` et `ContactRequest.item_name`, pour que l'historique des autres membres reste lisible ; `Report.reason`, pour la modération (intérêt légitime, indiqué dans la politique).

*Alternative écartée* : supprimer physiquement les objets et les demandes. Ça casserait l'historique des autres membres, qui doivent voir « Utilisateur supprimé ».

### 4. Textes rédigés directement dans les templates

Le contenu légal est du texte statique en français, sans traduction prévue. Le stocker en base ou en fichier Markdown serait une complexité inutile.

## Risks / Trade-offs

- [Un robot qui exécute JS récupère quand même l'email] → limite acceptée ; un alias Proton dédié resterait la meilleure parade si le spam arrive.
- [Les durées et sous-traitants de la page deviennent faux si l'infra change (Gmail → autre SMTP, région Railway)] → la page indique une date de dernière mise à jour ; tout futur change d'infra devra mettre à jour la politique.
- [Le message déjà envoyé par email au propriétaire reste dans sa boîte] → impossible à corriger côté serveur ; la politique le signale.
- [Les comptes supprimés avant ce change gardent leurs descriptions et messages] → volume négligeable en alpha. Pas de migration de données ; un nettoyage manuel reste possible depuis le shell si besoin.

## Migration Plan

Déploiement standard par push. Aucune migration de base, aucune variable d'environnement. Retour arrière : revert du commit.
