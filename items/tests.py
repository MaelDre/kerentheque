from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.factories import make_category, make_item, make_neighborhood, make_user
from contacts.models import ContactRequest
from contacts.services import refuse, send_request

from .models import Item
from .search import normalize


class NormalizeTests(TestCase):
    def test_lowercase_and_strip_accents(self):
        self.assertEqual(normalize("Échelle Télescopique"), "echelle telescopique")


class ItemManagementTests(TestCase):
    def setUp(self):
        self.owner = make_user()
        self.category = make_category()
        self.client.force_login(self.owner)

    def test_create_item(self):
        response = self.client.post(
            reverse("items:create"), {"name": "Scie sauteuse", "category": self.category.pk, "description": ""}
        )
        item = Item.objects.get()
        self.assertRedirects(response, item.get_absolute_url())
        self.assertEqual(item.owner, self.owner)
        self.assertTrue(Item.objects.available().filter(pk=item.pk).exists())

    def test_required_fields(self):
        response = self.client.post(reverse("items:create"), {"name": "", "category": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Item.objects.exists())

    def test_inactive_category_refused(self):
        inactive = make_category(is_active=False)
        self.client.post(reverse("items:create"), {"name": "Scie", "category": inactive.pk})
        self.assertFalse(Item.objects.exists())

    def test_anonymous_redirected_to_login(self):
        self.client.logout()
        response = self.client.get(reverse("items:create"))
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + reverse("items:create"))

    def test_mine_lists_only_own_items(self):
        mine = make_item(owner=self.owner, name="Ma tente")
        make_item(name="Tente du voisin")
        deleted = make_item(owner=self.owner, name="Vieux vélo")
        deleted.deleted_at = deleted.created_at
        deleted.save()
        response = self.client.get(reverse("items:mine"))
        self.assertContains(response, mine.name)
        self.assertNotContains(response, "Tente du voisin")
        self.assertNotContains(response, "Vieux vélo")

    def test_edit_item(self):
        item = make_item(owner=self.owner, category=self.category)
        self.client.post(
            reverse("items:edit", args=[item.pk]),
            {"name": item.name, "category": self.category.pk, "description": "Avec deux batteries"},
        )
        item.refresh_from_db()
        self.assertEqual(item.description, "Avec deux batteries")
        self.assertIn("batteries", item.search_text)

    def test_edit_by_other_user_forbidden(self):
        item = make_item()
        self.assertEqual(self.client.get(reverse("items:edit", args=[item.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("items:delete", args=[item.pk])).status_code, 404)

    def test_delete_item_cancels_pending_requests_silently(self):
        item = make_item(owner=self.owner)
        pending = send_request(make_user(), item)
        refused = send_request(make_user(), item)
        refuse(refused, self.owner)
        mail.outbox.clear()

        response = self.client.post(reverse("items:delete", args=[item.pk]))
        self.assertRedirects(response, reverse("items:mine"))
        item.refresh_from_db()
        self.assertIsNotNone(item.deleted_at)
        pending.refresh_from_db()
        refused.refresh_from_db()
        self.assertEqual(pending.status, ContactRequest.Status.CANCELLED)
        self.assertEqual(refused.status, ContactRequest.Status.REFUSED)
        self.assertEqual(mail.outbox, [])

        # La demande annulée reste visible, avec le nom de l'objet, chez le demandeur.
        self.client.force_login(pending.requester)
        response = self.client.get(reverse("contacts:sent"))
        self.assertContains(response, item.name)
        self.assertContains(response, "Annulée")


class CatalogTests(TestCase):
    def setUp(self):
        self.centre = make_neighborhood("Centre")
        self.port = make_neighborhood("Port")
        self.bricolage = make_category("Outillage")
        self.jardin = make_category("Jardin")
        self.alice = make_user(pseudo="Alice", neighborhood=self.centre, email="alice@example.com", phone="0611111111")
        self.bob = make_user(pseudo="Bob", neighborhood=self.port)

    def catalog(self, **params):
        return self.client.get(reverse("items:catalog"), params)

    def test_anonymous_sees_catalog(self):
        make_item(owner=self.alice, name="Perceuse")
        response = self.catalog()
        self.assertContains(response, "Perceuse")
        self.assertContains(response, "Centre")
        self.assertNotContains(response, "Alice")

    def test_member_sees_owner_in_catalog(self):
        make_item(owner=self.alice, name="Perceuse")
        self.client.force_login(self.bob)
        response = self.catalog()
        self.assertContains(response, "Alice")
        self.assertContains(response, "Centre")

    def test_no_private_data_exposed(self):
        item = make_item(owner=self.alice)
        for url in [reverse("items:catalog"), item.get_absolute_url()]:
            response = self.client.get(url)
            self.assertNotContains(response, "alice@example.com")
            self.assertNotContains(response, "0611111111")

    def test_deleted_and_suspended_items_hidden(self):
        deleted = make_item(owner=self.alice, name="Objet supprimé")
        deleted.deleted_at = deleted.created_at
        deleted.save()
        make_item(owner=self.bob, name="Objet de Bob")
        self.bob.is_active = False
        self.bob.save()
        response = self.catalog()
        self.assertNotContains(response, "Objet supprimé")
        self.assertNotContains(response, "Objet de Bob")
        self.assertEqual(self.client.get(deleted.get_absolute_url()).status_code, 404)

    def test_search_ignores_case_and_accents(self):
        make_item(owner=self.alice, name="Échelle", description="Trois mètres")
        make_item(owner=self.alice, name="Ponceuse")
        response = self.catalog(q="echelle")
        self.assertContains(response, "Échelle")
        self.assertNotContains(response, "Ponceuse")
        self.assertContains(self.catalog(q="METRES"), "Échelle")

    def test_search_without_result(self):
        self.assertContains(self.catalog(q="introuvable"), "Aucun objet ne correspond")

    def test_combined_filters(self):
        make_item(owner=self.alice, name="Scie circulaire", category=self.bricolage)
        make_item(owner=self.bob, name="Scie égoïne", category=self.bricolage)
        make_item(owner=self.alice, name="Scie à branches", category=self.jardin)
        response = self.catalog(q="scie", category=self.bricolage.pk, neighborhood=self.centre.pk)
        self.assertContains(response, "Scie circulaire")
        self.assertNotContains(response, "Scie égoïne")
        self.assertNotContains(response, "Scie à branches")

    @override_settings(CATALOG_PAGE_SIZE=2)
    def test_pagination_keeps_filters(self):
        for i in range(3):
            make_item(owner=self.alice, name=f"Outil {i}")
        response = self.catalog(q="outil")
        self.assertContains(response, "q=outil&amp;page=2")

    def test_detail_for_anonymous_invites_login(self):
        item = make_item(owner=self.alice)
        response = self.client.get(item.get_absolute_url())
        self.assertContains(response, "Se connecter pour contacter le prêteur")
        self.assertContains(response, "Centre")
        self.assertNotContains(response, "Alice")

    def test_detail_for_member_shows_owner(self):
        item = make_item(owner=self.alice)
        self.client.force_login(self.bob)
        response = self.client.get(item.get_absolute_url())
        self.assertContains(response, "Prêté par <strong>Alice</strong>")
        self.assertContains(response, "Centre")

    def test_detail_for_owner_has_no_request_form(self):
        item = make_item(owner=self.alice)
        self.client.force_login(self.alice)
        response = self.client.get(item.get_absolute_url())
        self.assertNotContains(response, "Envoyer ma demande")
        self.assertContains(response, reverse("items:edit", args=[item.pk]))

    def test_detail_for_member_shows_request_form_and_shared_contact(self):
        item = make_item(owner=self.alice)
        self.client.force_login(self.bob)
        response = self.client.get(item.get_absolute_url())
        self.assertContains(response, "Envoyer ma demande")
        self.assertContains(response, self.bob.email)


class ErrorPagesTests(TestCase):
    def test_404_uses_site_template(self):
        response = self.client.get("/objets/999/")
        self.assertContains(response, "Page ou objet introuvable", status_code=404)

    def test_500_template_renders(self):
        from django.template.loader import render_to_string

        self.assertIn("Une erreur est survenue", render_to_string("500.html"))
