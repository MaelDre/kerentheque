## Why

Les habitants d'un même secteur possèdent de nombreux objets peu utilisés (outils, matériel de camping, appareils ménagers…) qu'ils accepteraient de prêter, mais n'ont aucun moyen simple de le faire savoir ni de trouver qui possède quoi. Kerentheque répond à ce besoin avec une web app minimale : un catalogue d'objets prêtables et une mise en relation soumise à l'accord du propriétaire. Le prêt lui-même se déroule hors de l'application.

Ce change pose le MVP complet, destiné à de vrais utilisateurs dans une zone géographique restreinte, avec pour priorité la simplicité fonctionnelle, technique et UX.

## What Changes

* Création d'une application web Django responsive (templates rendus côté serveur, Pico CSS, sans framework JS), base SQLite.
* Comptes utilisateurs avec connexion par lien magique envoyé par email (pas de mot de passe).
* Profil : pseudo et quartier (publics), email et téléphone facultatif (privés), réglages de partage des coordonnées (email et/ou téléphone, au moins un canal).
* Gestion par chaque utilisateur de ses objets prêtables : nom, catégorie, description. Tous les objets sont publics. Suppression logique.
* Catalogue public des objets avec recherche texte et filtres par catégorie et par quartier ; seuls le pseudo et le quartier du propriétaire sont affichés.
* Demandes de contact : le demandeur envoie une demande (message facultatif) en consentant à transmettre ses coordonnées ; le propriétaire est notifié par email et accepte ou refuse. En cas d'acceptation, le demandeur reçoit par email les coordonnées partagées par le propriétaire. Refus et annulation (objet supprimé) ne sont pas notifiés et restent visibles dans l'application.
* Garde-fous : limite de demandes en attente, pas de demande en double sur un même objet, signalement d'objets et d'utilisateurs, modération et gestion des listes de référence (catégories, quartiers) via l'admin Django, suppression de compte.

## Capabilities

### New Capabilities

* `user-accounts` : inscription et connexion par lien magique, profil (pseudo, quartier, email, téléphone), réglages de partage des coordonnées, suppression de compte.
* `item-management` : ajout, modification et suppression (logique) par un utilisateur de ses objets prêtables.
* `catalog` : consultation publique des objets disponibles, recherche texte et filtres par catégorie et par quartier.
* `contact-requests` : cycle de vie des demandes de contact (envoi, acceptation, refus, annulation), échange des coordonnées, notifications email, pages « Mes demandes » et « Demandes reçues », garde-fous anti-abus.
* `moderation` : signalement d'objets et d'utilisateurs, administration des catégories et quartiers, actions de modération.

### Modified Capabilities

<!-- Aucune : premier change du projet. -->

## Impact

* Nouveau projet Django (aucun code existant).
* Dépendances : Django, éventuellement `django-sesame` pour le lien magique ; Pico CSS servi en fichier statique.
* Base SQLite dont le chemin est configurable par variable d'environnement.
* Nécessite un moyen d'envoyer des emails (backend console en développement ; service transactionnel choisi au déploiement).
* Données personnelles (email, téléphone) transmises entre utilisateurs : consentement explicite, suppression de compte, pages mentions légales et confidentialité.
* Hors périmètre : hébergement et déploiement (Railway envisagé), choix du service d'emails, objets privés, photos, multi-villes, suivi du prêt, avis et réputation.