## Why

Aujourd'hui, n'importe quel visiteur non connecté peut consulter le catalogue et voir le pseudo du propriétaire de chaque objet. Il est donc possible d'établir, sans compte et sans aucune trace, la liste des objets détenus par une personne donnée. Réserver l'identité des propriétaires aux membres connectés limite cette exposition, tout en laissant le catalogue ouvert pour donner envie de s'inscrire.

## What Changes

- Le catalogue reste consultable sans être connecté, mais les cartes d'objets n'affichent plus le pseudo du propriétaire aux visiteurs non connectés.
- La fiche d'un objet vue par un visiteur non connecté n'affiche plus le pseudo du propriétaire, y compris dans l'invitation à se connecter (« Se connecter pour contacter le prêteur » au lieu de « … contacter Alice »).
- Le quartier du propriétaire reste visible et filtrable pour tous : il situe l'objet sans identifier une personne.
- Les membres connectés continuent de voir le pseudo et le quartier, sans changement.
- Les textes qui promettent un affichage « public » du pseudo (formulaire d'ajout d'objet, politique de confidentialité) sont mis à jour pour refléter la nouvelle règle.

## Capabilities

### New Capabilities

_Aucune._

### Modified Capabilities

- `catalog` : la consultation du catalogue et la fiche d'un objet distinguent désormais les visiteurs non connectés, qui ne voient plus le pseudo du propriétaire.
- `user-accounts` : la règle de visibilité du profil change. Le quartier reste public, le pseudo n'est plus visible que par les membres connectés.

## Impact

- Gabarits : `items/templates/items/item_card.html`, `items/templates/items/detail.html`, `items/templates/items/form.html`, `accounts/templates/accounts/privacy.html`.
- Tests : `items/tests.py` (`CatalogTests`, dont `test_anonymous_sees_catalog` qui vérifie actuellement la présence du pseudo).
- Aucun changement de modèle, de migration, d'URL ou de dépendance.
