"""Paliers du compteur d'objets affiché sur l'accueil (voir la spec catalog)."""

from dataclasses import dataclass

MILESTONES = (25, 50, 100, 200, 300, 400, 500, 700, 1000)

# Pourcentage à partir duquel le palier est signalé comme « Bientôt atteint ».
CLOSE_THRESHOLD_PERCENT = 80


@dataclass(frozen=True)
class MilestoneProgress:
    target: int
    percent: int
    missing: int
    is_close: bool


def milestone_progress(count):
    """Progression vers le prochain palier, ou None si le dernier palier est atteint."""
    target = next((milestone for milestone in MILESTONES if milestone > count), None)
    if target is None:
        return None
    # Pourcentage mesuré depuis 0 (et non depuis le palier précédent), arrondi à l'entier inférieur.
    percent = count * 100 // target
    return MilestoneProgress(
        target=target,
        percent=percent,
        missing=target - count,
        is_close=percent >= CLOSE_THRESHOLD_PERCENT,
    )
