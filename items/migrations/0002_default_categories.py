from django.db import migrations

DEFAULT_CATEGORIES = [
    "Bricolage",
    "Jardinage",
    "Cuisine",
    "Maison",
    "Sport et loisirs",
    "Camping et plein air",
    "Enfants",
    "Jeux",
    "Livres et films",
    "Électronique",
    "Fête et réception",
    "Autre",
]


def create_categories(apps, schema_editor):
    Category = apps.get_model("items", "Category")
    for position, name in enumerate(DEFAULT_CATEGORIES):
        Category.objects.get_or_create(name=name, defaults={"position": position * 10})


class Migration(migrations.Migration):
    dependencies = [("items", "0001_initial")]

    operations = [migrations.RunPython(create_categories, migrations.RunPython.noop)]
