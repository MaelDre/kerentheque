## MODIFIED Requirements

### Requirement: Consultation du catalogue
Le système MUST afficher, y compris aux visiteurs non connectés, la liste des objets disponibles : objets non supprimés dont le propriétaire a un compte actif (ni supprimé, ni suspendu). Chaque entrée MUST afficher le nom de l'objet, sa catégorie et le quartier du propriétaire. Pour un membre connecté, chaque entrée MUST en plus afficher le pseudo du propriétaire. Pour un visiteur non connecté, le pseudo du propriétaire MUST NOT apparaître nulle part dans la page. Les objets les plus récents apparaissent en premier, et la liste est paginée par 20 objets.

#### Scenario: Visiteur non connecté
- **WHEN** un visiteur non connecté ouvre le catalogue
- **THEN** il voit la liste des objets disponibles, avec leur nom, leur catégorie et le quartier du propriétaire
- **AND** le pseudo d'aucun propriétaire n'apparaît dans la page

#### Scenario: Membre connecté
- **WHEN** un membre connecté ouvre le catalogue
- **THEN** chaque objet affiche le pseudo et le quartier de son propriétaire

#### Scenario: Objet supprimé
- **WHEN** un objet a été supprimé par son propriétaire ou par la modération
- **THEN** il n'apparaît plus dans le catalogue

#### Scenario: Propriétaire suspendu
- **WHEN** le compte du propriétaire d'un objet est suspendu
- **THEN** ses objets n'apparaissent plus dans le catalogue

### Requirement: Fiche d'un objet
Le système MUST fournir une page de détail par objet, affichant son nom, sa catégorie, sa description et le quartier du propriétaire. Pour un membre connecté, la fiche MUST en plus afficher le pseudo du propriétaire. Pour un membre connecté qui n'est pas le propriétaire, la fiche MUST proposer l'envoi d'une demande de contact, ou indiquer le statut de sa demande existante. Pour un visiteur non connecté, elle MUST proposer de se connecter, et le pseudo du propriétaire MUST NOT apparaître nulle part dans la page.

#### Scenario: Fiche vue par un visiteur
- **WHEN** un visiteur non connecté ouvre la fiche d'un objet
- **THEN** il voit le nom, la catégorie, la description de l'objet et le quartier du propriétaire, ainsi qu'une invitation à se connecter pour contacter le prêteur
- **AND** le pseudo du propriétaire n'apparaît pas dans la page

#### Scenario: Fiche vue par un membre
- **WHEN** un membre connecté qui n'est pas le propriétaire ouvre la fiche d'un objet
- **THEN** il voit le pseudo et le quartier du propriétaire, et peut lui envoyer une demande de contact

#### Scenario: Fiche vue par le propriétaire
- **WHEN** le propriétaire ouvre la fiche de son propre objet
- **THEN** aucune demande de contact n'est proposée, et un accès à la modification est affiché

#### Scenario: Objet indisponible
- **WHEN** quelqu'un ouvre l'adresse d'un objet supprimé ou appartenant à un compte suspendu
- **THEN** le système affiche une page « objet introuvable »
