## Purpose

Définit le contenu obligatoire des mentions légales et de la politique de confidentialité de Kerentheque, ainsi que la protection de l'email de contact de l'éditeur contre la collecte automatique.

## ADDED Requirements

### Requirement: Contenu des mentions légales
La page des mentions légales MUST indiquer :
- l'éditeur : son nom (Maël Dréano), sa qualité d'éditeur non professionnel et son email de contact ;
- l'hébergeur : sa raison sociale (Railway Corporation), son adresse (548 Market St PMB 68956, San Francisco, CA 94104, États-Unis) et la localisation des serveurs (Pays-Bas, Union européenne) ;
- les conditions d'utilisation du service.

La page MUST NOT afficher l'adresse postale ni le numéro de téléphone de l'éditeur.

#### Scenario: Consultation des mentions légales
- **WHEN** un visiteur ouvre la page des mentions légales
- **THEN** il voit le nom de l'éditeur, son email de contact, la raison sociale et l'adresse de l'hébergeur, la localisation des serveurs et les conditions d'utilisation, sans adresse ni téléphone de l'éditeur

### Requirement: Contenu de la politique de confidentialité
La politique de confidentialité MUST indiquer :
- le responsable du traitement (nom de l'éditeur) et l'email de contact pour exercer ses droits ;
- les données collectées et leur visibilité ;
- les finalités et leurs bases légales : exécution du service (compte, mise en relation, emails de connexion et de notification) et intérêt légitime (modération, messages envoyés à l'éditeur) ;
- les règles de transmission des coordonnées entre membres ;
- les durées de conservation : données du compte jusqu'à sa suppression ; comptes jamais utilisés supprimés automatiquement après une semaine au minimum ; ce qui est effacé et ce qui est conservé à la suppression du compte, y compris le fait que les emails déjà envoyés à d'autres membres ne peuvent pas être rappelés ;
- les sous-traitants : Railway (hébergement, serveurs aux Pays-Bas) et Google via Gmail (envoi des emails, transfert vers les États-Unis encadré par le Data Privacy Framework UE–États-Unis) ;
- les cookies : uniquement des cookies strictement nécessaires (session et protection CSRF), sans mesure d'audience ni publicité ;
- les droits des personnes (accès, rectification, effacement, opposition, limitation, portabilité) et le droit d'introduire une réclamation auprès de la CNIL.

La politique MUST NOT annoncer de durée de conservation plus courte que celle réellement appliquée.

#### Scenario: Consultation de la politique de confidentialité
- **WHEN** un visiteur ouvre la politique de confidentialité
- **THEN** il y trouve le responsable du traitement et son email de contact, les finalités, les durées de conservation, les sous-traitants, les cookies utilisés et ses droits, dont le recours auprès de la CNIL

#### Scenario: Information sur la suppression de compte
- **WHEN** un visiteur lit la section sur la suppression de compte
- **THEN** il apprend que ses coordonnées, son pseudo, son quartier, les descriptions de ses objets et les messages de ses demandes sont effacés, et que le nom de ses objets et les motifs de ses signalements sont conservés sans ses coordonnées

### Requirement: Email de contact protégé contre la collecte automatique
L'email de contact de l'éditeur MUST NOT apparaître en clair, sous une forme complète et directement exploitable, dans le HTML servi par le serveur ni dans les fichiers du dépôt. Avec JavaScript activé, il MUST s'afficher comme un lien email cliquable. Sans JavaScript, la page MUST afficher une forme lisible par un humain (par exemple « mael.dreano [at] pm.me »).

#### Scenario: Visiteur avec JavaScript
- **WHEN** un visiteur dont le navigateur exécute JavaScript ouvre les mentions légales ou la politique de confidentialité
- **THEN** l'email de contact s'affiche comme un lien cliquable qui ouvre sa messagerie

#### Scenario: Robot qui lit le HTML sans exécuter JavaScript
- **WHEN** un client récupère le HTML de ces pages sans exécuter JavaScript
- **THEN** la réponse ne contient pas l'adresse `mael.dreano@pm.me` en clair ni de lien `mailto:` vers elle

#### Scenario: Visiteur sans JavaScript
- **WHEN** un visiteur dont JavaScript est désactivé ouvre ces pages
- **THEN** il voit une forme de l'email lisible par un humain
