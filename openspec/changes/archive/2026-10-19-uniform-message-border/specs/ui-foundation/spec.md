## ADDED Requirements

### Requirement: Cadre uniforme des messages d'état
Les messages d'état affichés en bandeau (confirmation, erreur, avertissement) MUST être encadrés d'un filet de même épaisseur sur les quatre côtés, sans accentuation d'un côté. La couleur de ce filet MUST dépendre du type de message : couleur principale pour un succès, couleur « danger » pour une erreur. Le texte du message reste le moyen principal de transmettre l'état.

#### Scenario: Confirmation d'une demande de prêt
- **WHEN** un membre envoie une demande de contact pour un objet
- **THEN** le message de confirmation s'affiche sur un fond teinté de la couleur principale, entouré d'un filet de la couleur principale de même épaisseur sur les quatre côtés

#### Scenario: Erreur de formulaire
- **WHEN** un formulaire est renvoyé avec une erreur
- **THEN** le bandeau d'erreur est entouré d'un filet de couleur « danger » de même épaisseur sur les quatre côtés
