## MODIFIED Requirements

### Requirement: Visibilité des informations de profil
Le système MUST n'afficher publiquement que le quartier d'un utilisateur. Le pseudo MUST n'être visible que par les membres connectés. L'email et le téléphone MUST rester privés et ne sont transmis à un autre utilisateur que dans le cadre d'une demande de contact.

#### Scenario: Consultation d'un objet par un visiteur non connecté
- **WHEN** un visiteur non connecté consulte un objet
- **THEN** seul le quartier du propriétaire est affiché, jamais son pseudo, son email ni son téléphone

#### Scenario: Consultation d'un objet par un membre
- **WHEN** un membre connecté consulte l'objet d'un autre membre
- **THEN** seuls le pseudo et le quartier du propriétaire sont affichés, jamais son email ni son téléphone
