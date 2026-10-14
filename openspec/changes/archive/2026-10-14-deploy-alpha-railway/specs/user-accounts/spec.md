## ADDED Requirements

### Requirement: Limitation des demandes de lien de connexion
Le système MUST envoyer au plus un lien de connexion par adresse email et par minute. Une demande faite moins d'une minute après la précédente pour la même adresse MUST être ignorée, sans envoi d'email, et MUST recevoir la même réponse qu'une demande normale. Cette limite MUST valoir pour toute l'application, quel que soit le nombre de processus qui servent les requêtes, et MUST continuer à s'appliquer après un redémarrage de l'application.

#### Scenario: Deux demandes rapprochées
- **WHEN** un visiteur demande deux liens de connexion pour le même email à moins d'une minute d'intervalle
- **THEN** un seul email est envoyé, et les deux demandes affichent le même message de confirmation

#### Scenario: Demandes traitées par des processus différents
- **WHEN** deux demandes pour le même email, à moins d'une minute d'intervalle, sont traitées par deux processus différents de l'application
- **THEN** un seul email est envoyé

#### Scenario: Redémarrage entre deux demandes
- **WHEN** l'application redémarre entre deux demandes pour le même email faites à moins d'une minute d'intervalle
- **THEN** un seul email est envoyé

#### Scenario: Nouvelle demande après une minute
- **WHEN** un visiteur redemande un lien pour le même email plus d'une minute après la demande précédente
- **THEN** un nouveau lien de connexion est envoyé
