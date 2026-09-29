# user-accounts Specification

## Purpose

Permet aux habitants de créer un compte sans mot de passe, de gérer leur profil public (pseudo, quartier) et leurs coordonnées privées, de choisir quelles coordonnées ils partagent, et de supprimer leur compte.

## Requirements

### Requirement: Connexion par lien magique
Le système MUST permettre à un visiteur de se connecter ou de s'inscrire en saisissant uniquement son adresse email. Le système MUST alors envoyer à cette adresse un lien de connexion à usage unique, valable 15 minutes. Aucun mot de passe n'est utilisé.

#### Scenario: Demande de lien pour un email connu
- **WHEN** un visiteur saisit l'email d'un compte existant et actif
- **THEN** le système envoie un lien de connexion à cet email et affiche un message l'invitant à consulter sa boîte mail

#### Scenario: Demande de lien pour un email inconnu
- **WHEN** un visiteur saisit un email qui ne correspond à aucun compte
- **THEN** le système envoie un lien de connexion à cet email et affiche le même message que pour un email connu, sans révéler si un compte existe

#### Scenario: Utilisation d'un lien valide
- **WHEN** un visiteur ouvre un lien de connexion valide et non utilisé
- **THEN** le système ouvre une session pour le compte associé à cet email, en créant le compte s'il n'existe pas encore

#### Scenario: Lien expiré ou déjà utilisé
- **WHEN** un visiteur ouvre un lien expiré ou déjà utilisé
- **THEN** le système refuse la connexion et propose de demander un nouveau lien

### Requirement: Complétion du profil à l'inscription
Le système MUST exiger d'un utilisateur nouvellement créé qu'il complète son profil avant d'accéder aux autres fonctionnalités réservées aux membres. Le profil comprend : un pseudo, un quartier choisi dans la liste des quartiers actifs, un numéro de téléphone facultatif, les réglages de partage des coordonnées, et l'acceptation des conditions d'utilisation et de la politique de confidentialité.

#### Scenario: Première connexion
- **WHEN** un utilisateur se connecte pour la première fois
- **THEN** le système le redirige vers le formulaire de complétion du profil

#### Scenario: Accès avant complétion
- **WHEN** un utilisateur au profil incomplet tente d'accéder à une page réservée aux membres
- **THEN** le système le redirige vers le formulaire de complétion du profil

#### Scenario: Conditions non acceptées
- **WHEN** un utilisateur soumet le formulaire sans accepter les conditions d'utilisation et la politique de confidentialité
- **THEN** le système refuse l'enregistrement et affiche une erreur

### Requirement: Pseudo unique
Le système MUST garantir que chaque pseudo est unique, sans distinction de casse. Le pseudo MUST contenir entre 3 et 30 caractères.

#### Scenario: Pseudo déjà pris
- **WHEN** un utilisateur choisit un pseudo déjà utilisé par un autre compte, quelle que soit la casse
- **THEN** le système refuse le pseudo et affiche une erreur

### Requirement: Visibilité des informations de profil
Le système MUST n'afficher publiquement que le quartier d'un utilisateur. Le pseudo MUST n'être visible que par les membres connectés. L'email et le téléphone MUST rester privés et ne sont transmis à un autre utilisateur que dans le cadre d'une demande de contact.

#### Scenario: Consultation d'un objet par un visiteur non connecté
- **WHEN** un visiteur non connecté consulte un objet
- **THEN** seul le quartier du propriétaire est affiché, jamais son pseudo, son email ni son téléphone

#### Scenario: Consultation d'un objet par un membre
- **WHEN** un membre connecté consulte l'objet d'un autre membre
- **THEN** seuls le pseudo et le quartier du propriétaire sont affichés, jamais son email ni son téléphone

### Requirement: Réglages de partage des coordonnées
Le système MUST permettre à l'utilisateur de choisir, depuis son profil, les coordonnées qu'il partage : email, téléphone, ou les deux. Au moins un canal MUST être sélectionné. Le partage du téléphone MUST n'être possible que si un numéro est renseigné. Ces réglages s'appliquent quand l'utilisateur envoie une demande comme quand il en accepte une.

#### Scenario: Aucun canal sélectionné
- **WHEN** un utilisateur enregistre ses réglages sans aucun canal sélectionné
- **THEN** le système refuse l'enregistrement et affiche une erreur

#### Scenario: Partage du téléphone sans numéro
- **WHEN** un utilisateur sélectionne le partage du téléphone sans avoir renseigné de numéro
- **THEN** le système refuse l'enregistrement et affiche une erreur

#### Scenario: Retrait du numéro de téléphone
- **WHEN** un utilisateur qui partage uniquement son téléphone supprime son numéro
- **THEN** le système refuse l'enregistrement tant qu'aucun autre canal n'est sélectionné

### Requirement: Modification du profil
Le système MUST permettre à l'utilisateur de modifier son pseudo, son quartier, son téléphone et ses réglages de partage, avec les mêmes règles de validation qu'à l'inscription. L'email de connexion n'est pas modifiable dans le MVP.

#### Scenario: Changement de quartier
- **WHEN** un utilisateur choisit un autre quartier actif et enregistre
- **THEN** le nouveau quartier est affiché sur ses objets dans le catalogue

### Requirement: Déconnexion
Le système MUST permettre à un utilisateur connecté de se déconnecter.

#### Scenario: Déconnexion
- **WHEN** un utilisateur connecté se déconnecte
- **THEN** sa session est fermée et il est redirigé vers le catalogue

### Requirement: Suppression de compte
Le système MUST permettre à l'utilisateur de supprimer son compte après confirmation. La suppression MUST effacer son email, son téléphone et son pseudo, retirer tous ses objets du catalogue, et annuler toutes les demandes en attente qu'il a envoyées ou reçues. Dans l'historique des autres utilisateurs, il MUST apparaître comme « Utilisateur supprimé ».

#### Scenario: Suppression confirmée
- **WHEN** un utilisateur confirme la suppression de son compte
- **THEN** ses données personnelles sont effacées, ses objets disparaissent du catalogue, ses demandes en attente sont annulées et sa session est fermée

#### Scenario: Reconnexion après suppression
- **WHEN** une personne demande un lien de connexion avec l'email d'un compte supprimé
- **THEN** le système la traite comme une nouvelle inscription, sans lien avec l'ancien compte

### Requirement: Pages légales
Le système MUST fournir, accessibles sans connexion, une page de mentions légales et une page de politique de confidentialité expliquant quelles données sont collectées et à qui elles sont transmises.

#### Scenario: Accès aux pages légales
- **WHEN** un visiteur ouvre le lien vers la politique de confidentialité depuis n'importe quelle page
- **THEN** la page s'affiche sans connexion requise
