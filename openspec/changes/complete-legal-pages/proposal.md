## Why

Les pages « Mentions légales » et « Politique de confidentialité » contiennent encore des textes provisoires avec des champs à remplir (`[Nom de l'éditeur]`, `[email de contact]`…). Il faut les compléter avant de partager l'application à un premier testeur. La politique actuelle annonce aussi un effacement plus complet que ce que fait réellement la suppression de compte : les descriptions d'objets et les messages de contact, qui sont des textes libres pouvant contenir des données personnelles, restent en base.

## What Changes

- **Mentions légales** : texte définitif. Éditeur non professionnel identifié par son nom et un email de contact, sans adresse postale ni téléphone (LCEN art. 6-III-2). Hébergeur : Railway Corporation (adresse aux États-Unis, serveurs aux Pays-Bas). Les conditions d'utilisation existantes sont conservées.
- **Politique de confidentialité** : texte définitif. Ajout du responsable du traitement et de son contact, des finalités et bases légales, des durées de conservation, des sous-traitants (Railway pour l'hébergement dans l'UE, Google/Gmail pour l'envoi des emails aux États-Unis), des cookies strictement nécessaires (donc sans bandeau), des droits RGPD et du recours auprès de la CNIL.
- **Email de contact protégé contre la collecte automatique** : l'adresse n'apparaît en clair ni dans le HTML servi ni dans le dépôt Git. Elle est assemblée côté navigateur, avec un texte de repli lisible quand JavaScript est désactivé.
- **Suppression de compte plus complète** : elle vide aussi la description des objets du membre et le texte des messages de ses demandes de contact, envoyées ou reçues. Les motifs des signalements rédigés par le membre sont conservés pour la modération. Le nom des objets est conservé pour l'historique des autres membres.

Hors périmètre : planification régulière (cron) de la purge des comptes inutilisés, remplacement de Gmail par un service d'envoi dédié, domaine personnalisé.

## Capabilities

### New Capabilities

- `legal-information` : contenu exigé des mentions légales et de la politique de confidentialité, et protection de l'email de contact contre la collecte automatique.

### Modified Capabilities

- `user-accounts` : l'exigence « Suppression de compte » s'étend aux textes libres (descriptions d'objets, messages de contact) et précise que les motifs de signalement sont conservés. L'exigence « Pages légales » renvoie à la nouvelle capability pour leur contenu.

## Impact

- Templates : `accounts/templates/accounts/legal.html`, `accounts/templates/accounts/privacy.html`, plus un nouveau fragment de template pour l'email protégé.
- Front : premier fichier JavaScript du projet (`static/js/`), petit et sans dépendance, chargé uniquement sur les pages qui en ont besoin.
- Code : `accounts/services.py` (`delete_account`) et ses tests.
- Aucune migration, aucune nouvelle dépendance, aucun changement de déploiement.
