## 1. Email protégé

- [x] 1.1 Ajouter un bloc `{% block scripts %}{% endblock %}` avant `</body>` dans `templates/base.html`
- [x] 1.2 Créer `templates/includes/protected_email.html` : lien avec `data-user` / `data-domain` et texte de repli « user [at] domain », sans adresse complète ni `mailto:` dans le HTML
- [x] 1.3 Créer `static/js/protected-email.js` : remplace chaque repli par un lien `mailto:` cliquable
- [x] 1.4 Test : le HTML des deux pages légales ne contient ni `mael.dreano@pm.me` ni `mailto:`, mais contient bien le repli lisible

## 2. Mentions légales

- [x] 2.1 Réécrire `accounts/templates/accounts/legal.html` : éditeur (Maël Dréano, non professionnel, email protégé), hébergeur (Railway Corporation, adresse, serveurs aux Pays-Bas), conditions d'utilisation conservées, date de mise à jour ; retirer le commentaire « TEXTE PROVISOIRE »
- [x] 2.2 Charger le script via le bloc `scripts`

## 3. Politique de confidentialité

- [x] 3.1 Réécrire `accounts/templates/accounts/privacy.html` avec toutes les sections exigées par la spec `legal-information` (responsable, données, finalités et bases légales, transmission des coordonnées, conservation, sous-traitants Railway et Gmail, cookies, droits et CNIL), plus la date de mise à jour ; retirer le commentaire « TEXTE PROVISOIRE »
- [x] 3.2 Décrire précisément ce qui est effacé et conservé à la suppression du compte, y compris les emails déjà envoyés aux autres membres
- [x] 3.3 Charger le script via le bloc `scripts`

## 4. Suppression de compte

- [x] 4.1 Dans `delete_account()` (`accounts/services.py`), vider la description des objets du membre et recalculer `search_text`
- [x] 4.2 Dans la même transaction, vider `message` des demandes de contact envoyées par le membre
- [x] 4.3 Tests : description et message vides après suppression, nom de l'objet conservé, signalement et motif conservés

## 5. Vérification

- [x] 5.1 Lancer toute la suite de tests
- [x] 5.2 Vérifier en local, avec et sans JavaScript, l'affichage de l'email sur les deux pages
