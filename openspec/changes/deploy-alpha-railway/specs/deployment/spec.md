## Purpose

Permet d'exécuter Kerentheque en production : l'application démarre de façon autonome, met à jour son schéma de base de données et conserve les données des membres d'un déploiement à l'autre.

## ADDED Requirements

### Requirement: Démarrage autonome en production
Le système MUST pouvoir être construit et démarré en production sans aucune intervention manuelle, à partir du seul code source et des variables d'environnement. Au démarrage, le système MUST appliquer les migrations de base de données en attente avant d'accepter des requêtes. Il MUST ensuite servir les requêtes avec un serveur d'application de production, sur le port fourni par l'hébergeur.

#### Scenario: Premier démarrage sur une base vide
- **WHEN** l'application démarre et qu'aucune base de données n'existe encore à l'emplacement configuré
- **THEN** la base est créée avec le schéma complet, catégories par défaut comprises, puis l'application répond aux requêtes

#### Scenario: Déploiement d'une version avec une nouvelle migration
- **WHEN** une nouvelle version contenant une migration est déployée sur une base existante
- **THEN** la migration est appliquée au démarrage, avant que la nouvelle version ne serve des pages

#### Scenario: Échec d'une migration
- **WHEN** une migration échoue au démarrage
- **THEN** l'application ne démarre pas, plutôt que de servir des pages sur un schéma incohérent

### Requirement: Persistance des données entre les déploiements
Le système MUST stocker sa base de données à un emplacement configurable par variable d'environnement, qui peut se trouver sur un stockage persistant indépendant de l'image de l'application. Les données (comptes, objets, demandes de contact, signalements) MUST être conservées lors d'un redéploiement ou d'un redémarrage.

#### Scenario: Redéploiement
- **WHEN** une nouvelle version de l'application est déployée
- **THEN** les comptes, objets et demandes existants sont toujours présents après le redémarrage

### Requirement: Purge des comptes inutilisés au démarrage
Le système MUST supprimer, à chaque démarrage, les comptes créés lors d'une demande de lien mais jamais utilisés pour se connecter, selon les règles de rétention existantes (comptes sans connexion ni pseudo, hors administrateurs, créés depuis plus de 7 jours).

#### Scenario: Compte jamais utilisé
- **WHEN** l'application démarre et qu'un compte a été créé il y a plus de 7 jours sans jamais avoir servi à se connecter
- **THEN** ce compte est supprimé

#### Scenario: Compte récent ou utilisé
- **WHEN** l'application démarre
- **THEN** les comptes créés depuis moins de 7 jours, les comptes ayant déjà servi à se connecter et les comptes administrateurs sont conservés

### Requirement: Fichiers statiques servis en production
Le système MUST servir lui-même ses fichiers statiques (CSS) en production, sans serveur web supplémentaire, avec `DEBUG` désactivé.

#### Scenario: Chargement d'une page en production
- **WHEN** un visiteur ouvre une page du site en production
- **THEN** la feuille de style est chargée et la page s'affiche avec sa mise en forme
