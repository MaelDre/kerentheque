"""Fabriques de données pour les tests."""

import itertools

from django.utils import timezone

from items.models import Category, Item

from .models import Neighborhood, User

_counter = itertools.count(1)


def make_neighborhood(name=None, **kwargs):
    return Neighborhood.objects.create(name=name or f"Quartier {next(_counter)}", **kwargs)


def make_category(name=None, **kwargs):
    return Category.objects.create(name=name or f"Catégorie {next(_counter)}", **kwargs)


def make_user(pseudo=None, neighborhood=None, complete=True, **kwargs):
    n = next(_counter)
    email = kwargs.pop("email", f"user{n}@example.com")
    if complete:
        kwargs.setdefault("pseudo", pseudo or f"membre{n}")
        kwargs.setdefault("neighborhood", neighborhood or make_neighborhood())
        kwargs.setdefault("terms_accepted_at", timezone.now())
    return User.objects.create_user(email, **kwargs)


def make_item(owner=None, name="Perceuse", category=None, **kwargs):
    return Item.objects.create(
        owner=owner or make_user(), name=name, category=category or make_category(), **kwargs
    )
