## Context

Le pseudo du propriétaire est rendu directement par les gabarits à partir de `item.owner.pseudo` : dans `item_card.html` (catalogue), dans l'en-tête de `detail.html` et dans le bouton de connexion destiné aux visiteurs de `detail.html`. Les vues `catalog` et `detail` sont publiques et chargent déjà `owner` avec `select_related`. Aucune API ni aucun flux de données ne publie le pseudo en dehors de ces gabarits.

## Goals / Non-Goals

**Goals:**
- Aucune occurrence du pseudo d'un propriétaire dans le HTML servi à un visiteur non connecté, sur le catalogue comme sur la fiche.
- Aucun changement pour les membres connectés.

**Non-Goals:**
- Masquer le quartier, ou supprimer le filtre par quartier.
- Distinguer les membres dont le profil est incomplet : tout utilisateur authentifié compte comme membre.
- Masquer l'identité dans d'autres espaces déjà réservés aux membres (demandes de contact, e-mails).

## Decisions

**Masquer dans les gabarits avec `user.is_authenticated`, sans toucher aux vues.**
Les deux gabarits disposent déjà de `user` via le processeur de contexte d'authentification. Un simple `{% if user.is_authenticated %}` autour du pseudo suffit et reste lisible. Alternative écartée : ne pas charger `owner` côté vue pour les anonymes. Le quartier vient de `owner.neighborhood`, il faudrait donc le charger de toute façon, et on ajouterait des branchements dans la vue pour un gain nul.

**Garder le quartier visible et filtrable.**
Un quartier regroupe beaucoup d'habitants. Il aide un visiteur à juger si un objet est proche, sans identifier personne, et le filtre par quartier du catalogue reste utile avant l'inscription. Alternative écartée : tout masquer. On perdrait l'intérêt du catalogue public, pour un bénéfice de confidentialité faible.

**Libellé neutre dans l'invitation à se connecter : « Se connecter pour contacter le prêteur ».**
Le bouton actuel cite le pseudo, ce qui contredirait la règle.

**Vérifier par des tests d'absence (`assertNotContains`) sur le pseudo.**
Le critère de la spec est « le pseudo n'apparaît nulle part dans la page ». Les tests vérifient donc la réponse complète pour un anonyme, sur le catalogue et sur la fiche, avec un pseudo distinctif.

## Risks / Trade-offs

- [Un futur gabarit public réaffiche `owner.pseudo` par inadvertance] → Les tests d'absence sur le catalogue et la fiche détectent la régression sur ces pages. Tout nouvel écran public devra ajouter le même test.
- [Des objets au nom très explicite (« Perceuse d'Alice ») contournent le masquage] → C'est un choix de l'utilisateur, hors du périmètre de la règle. Le texte du formulaire d'ajout reste neutre à ce sujet.
- [Le quartier combiné à un objet rare peut suffire à identifier quelqu'un dans un petit quartier] → Risque accepté. Le quartier était déjà public et ce changement ne l'aggrave pas.
