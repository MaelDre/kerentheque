import unicodedata


def normalize(text):
    """Met un texte en minuscules et retire les accents, pour une recherche tolérante."""
    decomposed = unicodedata.normalize("NFKD", text or "")
    return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()
