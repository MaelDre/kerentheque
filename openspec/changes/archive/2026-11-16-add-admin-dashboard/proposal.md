## Why

L'administration (`/admin/`) permet déjà d'agir sur la plateforme : traiter les signalements, retirer des objets, suspendre des comptes. En revanche, elle ne donne aucune vue d'ensemble de l'activité. Pendant l'alpha, il faut pouvoir suivre en un coup d'œil si la plateforme est utilisée, sans lancer de requêtes SQL à la main.

## What Changes

- Ajout d'un tableau de bord en tête de la page d'accueil de l'administration, avec quatre indicateurs :
  - **Objets** : objets non supprimés ;
  - **Membres inscrits** : comptes actifs (non suspendus, non supprimés) dont le profil est complet ;
  - **Demandes de prêt** : toutes les demandes de contact, quel que soit leur statut ;
  - **Mises en relation acceptées** : demandes au statut « acceptée ». Ce statut indique que les coordonnées ont été échangées, pas que le prêt a eu lieu, d'où ce libellé.
- Ces indicateurs ne sont visibles que des super-administrateurs. Les autres administrateurs (il n'y en a pas pour l'instant) gardent l'accès à l'administration, sans les indicateurs.
- Les actions disponibles dans l'administration ne changent pas.

## Capabilities

### New Capabilities

_Aucune._

### Modified Capabilities

- `moderation` : ajout d'une exigence « Tableau de bord des indicateurs » réservée aux super-administrateurs.

## Impact

- Page d'accueil de l'administration Django : nouveau template qui étend celui par défaut.
- `moderation` : une fonction de calcul des indicateurs et son affichage.
- `config/urls.py` : déclaration du template d'accueil de l'administration.
- Aucune migration, aucune nouvelle dépendance, aucune nouvelle URL publique.
