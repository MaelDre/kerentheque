from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from accounts.models import Neighborhood, User
from items.models import Category, Item

NEIGHBORHOODS = ["Centre-ville", "Gare", "Port", "Quartier nord", "Quartier sud"]

MEMBERS = [
    ("alice@example.com", "Alice", "Centre-ville", [
        ("Perceuse à percussion", "Bricolage", "Avec un jeu de forets béton et bois."),
        ("Tente 4 places", "Camping et plein air", "Montage facile, sac de transport inclus."),
    ]),
    ("bernard@example.com", "Bernard", "Port", [
        ("Échelle télescopique 3 m", "Bricolage", ""),
        ("Appareil à raclette 8 personnes", "Cuisine", "Poêlons et spatules fournis."),
        ("Tondeuse électrique", "Jardinage", "Câble de 20 m."),
    ]),
]


class Command(BaseCommand):
    help = "Crée des quartiers, des membres et des objets de démonstration (développement uniquement)."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Commande réservée au développement (DEBUG=true).")

        for position, name in enumerate(NEIGHBORHOODS):
            Neighborhood.objects.get_or_create(name=name, defaults={"position": position * 10})

        for email, pseudo, neighborhood, items in MEMBERS:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "pseudo": pseudo,
                    "neighborhood": Neighborhood.objects.get(name=neighborhood),
                    "terms_accepted_at": timezone.now(),
                },
            )
            if created:
                user.set_unusable_password()
                user.save()
                for name, category, description in items:
                    Item.objects.create(
                        owner=user, name=name, category=Category.objects.get(name=category), description=description
                    )

        self.stdout.write(self.style.SUCCESS(
            f"{len(NEIGHBORHOODS)} quartiers et {len(MEMBERS)} membres de démonstration prêts "
            "(alice@example.com, bernard@example.com : connexion par lien magique affiché dans la console)."
        ))
