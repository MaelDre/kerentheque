## ADDED Requirements

### Requirement: Tableau de bord des indicateurs
La page d'accueil de l'interface d'administration MUST afficher aux super-administrateurs quatre indicateurs calculés au moment de l'affichage :
- **Objets** : nombre d'objets non supprimés, y compris ceux des comptes suspendus ;
- **Membres inscrits** : nombre de comptes actifs, non supprimés et dont le profil est complet (pseudo, quartier et conditions acceptées) ;
- **Demandes de prêt** : nombre total de demandes de contact, tous statuts confondus ;
- **Mises en relation acceptées** : nombre de demandes de contact au statut « acceptée ».

Ces indicateurs MUST NOT être affichés aux administrateurs qui ne sont pas super-administrateurs.

#### Scenario: Super-administrateur sur l'accueil de l'administration
- **WHEN** un super-administrateur ouvre la page d'accueil de l'administration
- **THEN** il voit les quatre indicateurs avec leur valeur, au-dessus de la liste des modules d'administration

#### Scenario: Objets supprimés exclus
- **WHEN** un objet a été supprimé par son propriétaire ou par la modération
- **THEN** il n'est plus compté dans l'indicateur « Objets »

#### Scenario: Comptes non comptés comme membres inscrits
- **WHEN** un compte a un profil incomplet, est suspendu ou a été supprimé
- **THEN** il n'est pas compté dans l'indicateur « Membres inscrits »

#### Scenario: Demandes comptées selon leur statut
- **WHEN** il existe une demande en attente, une acceptée, une refusée et une annulée
- **THEN** l'indicateur « Demandes de prêt » vaut 4 et l'indicateur « Mises en relation acceptées » vaut 1

#### Scenario: Administrateur sans droits de super-administrateur
- **WHEN** un administrateur qui n'est pas super-administrateur ouvre la page d'accueil de l'administration
- **THEN** il accède à l'administration, mais aucun indicateur n'est affiché
