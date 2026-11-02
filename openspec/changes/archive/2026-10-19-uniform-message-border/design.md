## Context

Un message d'état est rendu comme un `<article>` : il hérite du style « carte » de `static/css/theme.css` (filet de 1px `border`, coins `radius-lg`). La classe `.message` de `static/css/site.css` remplace ensuite le côté gauche par une barre de `space-1` (4px) colorée selon le type. C'est cette surcharge qui crée l'accentuation.

Aujourd'hui, le message d'erreur n'a pas de fond : sa barre rouge est son seul repère coloré.

## Goals / Non-Goals

**Goals:**
- Un cadre de même épaisseur sur les quatre côtés pour tous les messages d'état.
- Garder un repère coloré pour chaque type, en particulier pour les erreurs.

**Non-Goals:**
- Ajouter un token au design system (par exemple une teinte rouge pâle pour le fond des erreurs).
- Modifier les templates ou le texte des messages.

## Decisions

- **Filet de 1px coloré selon le type, plutôt que neutre pour tous.** On garde l'épaisseur du filet des cartes (`--pico-border-width`) et on change seulement sa couleur : `brand` pour un succès, `danger` pour une erreur. Alternative écartée : un filet neutre `border` partout avec un fond rouge pâle pour les erreurs. Elle demandait un nouveau token, et l'erreur aurait perdu tout repère tant que ce token n'existe pas.
- **Avertissement en `border-strong` plutôt qu'en `ink`.** Un filet `ink` sur les quatre côtés serait trop dur. Le fond `surface-sunken` suffit à distinguer l'avertissement, et `border-strong` reste un token prévu pour les bordures.
- **On s'appuie sur la bordure héritée de `article`.** `.message` ne redéfinit que `border-color` : l'épaisseur et les coins restent ceux des cartes, sans duplication.
- **Bordure de repli pour un type inconnu.** Un message sans type connu (par exemple `info`) garde le filet neutre `border` des cartes.

## Risks / Trade-offs

- [Un filet de 1px est moins visible qu'une barre de 4px] → c'est l'effet recherché ; le texte porte le sens (exigence « État jamais porté par la seule couleur ») et la couleur ne fait que le renforcer.
