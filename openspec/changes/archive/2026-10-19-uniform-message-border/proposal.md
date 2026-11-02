## Why

Les messages d'état (confirmation d'une demande de prêt, erreurs de formulaire…) ont une barre colorée de 4px sur leur bord gauche, qui s'ajoute au filet fin des cartes. Cet effet d'accentuation n'apporte rien à la lecture et alourdit l'interface : le cadre doit être uni sur les quatre côtés.

## What Changes

- Retirer la barre épaisse du bord gauche des messages d'état.
- Encadrer chaque message d'un filet fin uniforme sur les quatre côtés, dont la couleur dépend du type : couleur principale pour un succès, couleur « danger » pour une erreur, bordure neutre renforcée pour un avertissement.
- Conserver les fonds actuels (teinte de la couleur principale pour un succès, surface en retrait pour un avertissement) et les coins arrondis des cartes.

## Capabilities

### New Capabilities
_Aucune._

### Modified Capabilities
- `ui-foundation` : ajout d'une exigence sur l'apparence des messages d'état (cadre uniforme sur les quatre côtés, couleur selon le type).

## Impact

- **CSS** : règles `.message` de `static/css/site.css`.
- **Écrans concernés** : tous les messages flash (`templates/base.html`) et le bandeau d'erreur des formulaires (`templates/includes/form_fields.html`). Aucun changement de template.
- **Dépendances** : aucune nouvelle.
