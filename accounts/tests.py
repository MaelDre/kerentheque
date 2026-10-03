import re
import time
from unittest import mock

from django.core import mail
from django.core.cache import cache, caches
from django.core.management import CommandError, call_command
from django.db import connection
from django.db.models import ProtectedError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from sesame.utils import get_query_string

from contacts.models import ContactRequest
from contacts.services import send_request
from items.models import Item

from .factories import make_category, make_item, make_neighborhood, make_user
from .forms import ProfileForm
from .models import Neighborhood, User
from .services import delete_account


def extract_link(message):
    return re.search(r"http://\S+", message.body).group(0)


class ReferenceDataTests(TestCase):
    def test_used_neighborhood_cannot_be_deleted(self):
        user = make_user()
        with self.assertRaises(ProtectedError):
            user.neighborhood.delete()

    def test_used_category_cannot_be_deleted(self):
        item = make_item()
        with self.assertRaises(ProtectedError):
            item.category.delete()


class MagicLinkTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_link_sent_for_known_email(self):
        user = make_user(email="alice@example.com")
        response = self.client.post(reverse("accounts:login"), {"email": "Alice@Example.com"})
        self.assertContains(response, "Consultez vos emails")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["alice@example.com"])
        self.assertIn(reverse("accounts:magic_link"), mail.outbox[0].body)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().pk, user.pk)

    def test_unknown_email_gets_same_response_and_creates_account(self):
        response = self.client.post(reverse("accounts:login"), {"email": "new@example.com"})
        self.assertContains(response, "Consultez vos emails")
        self.assertEqual(len(mail.outbox), 1)
        self.assertFalse(User.objects.get(email="new@example.com").is_profile_complete)

    def test_link_requests_are_throttled(self):
        self.client.post(reverse("accounts:login"), {"email": "a@example.com"})
        self.client.post(reverse("accounts:login"), {"email": "a@example.com"})
        self.assertEqual(len(mail.outbox), 1)

    def test_throttle_is_shared_and_expires(self):
        self.client.post(reverse("accounts:login"), {"email": "a@example.com"})
        # Une autre connexion au cache (comme celle d'un autre processus) voit la limite.
        self.assertIsNotNone(caches.create_connection("default").get("login-link:a@example.com"))
        # Une minute plus tard, la limite a expiré et un nouveau lien est envoyé.
        with connection.cursor() as cursor:
            cursor.execute("UPDATE django_cache SET expires = %s", [timezone.now() - timezone.timedelta(seconds=1)])
        self.client.post(reverse("accounts:login"), {"email": "a@example.com"})
        self.assertEqual(len(mail.outbox), 2)

    def test_get_does_not_consume_link_and_post_logs_in(self):
        user = make_user()
        url = reverse("accounts:magic_link") + get_query_string(user)
        self.assertContains(self.client.get(url), "Me connecter")
        self.assertContains(self.client.get(url), "Me connecter")  # toujours valide
        token = url.split("sesame=")[1]
        response = self.client.post(reverse("accounts:magic_link"), {"sesame": token})
        self.assertRedirects(response, reverse("items:catalog"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_link_is_single_use(self):
        user = make_user()
        token = get_query_string(user).split("sesame=")[1]
        self.client.post(reverse("accounts:magic_link"), {"sesame": token})
        self.client.logout()
        response = self.client.post(reverse("accounts:magic_link"), {"sesame": token})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "n'est plus valable", status_code=400)

    def test_expired_link_is_refused(self):
        user = make_user()
        token = get_query_string(user).split("sesame=")[1]
        later = time.time() + 16 * 60
        with mock.patch("sesame.tokens_v2.time.time", return_value=later):
            response = self.client.post(reverse("accounts:magic_link"), {"sesame": token})
        self.assertEqual(response.status_code, 400)

    def test_first_login_redirects_to_profile(self):
        self.client.post(reverse("accounts:login"), {"email": "new@example.com"})
        link = extract_link(mail.outbox[0])
        token = link.split("sesame=")[1]
        response = self.client.post(reverse("accounts:magic_link"), {"sesame": token})
        self.assertRedirects(response, reverse("accounts:profile"))

    def test_suspended_account_cannot_log_in(self):
        user = make_user(email="bob@example.com")
        token = get_query_string(user).split("sesame=")[1]
        user.is_active = False
        user.save()
        self.client.post(reverse("accounts:login"), {"email": "bob@example.com"})
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(reverse("accounts:magic_link"), {"sesame": token})
        self.assertEqual(response.status_code, 400)


class ProfileTests(TestCase):
    def setUp(self):
        self.neighborhood = make_neighborhood()

    def form(self, user, **data):
        base = {"pseudo": "Alice", "neighborhood": self.neighborhood.pk, "phone": "", "share_email": "on"}
        base.update(data)
        return ProfileForm({k: v for k, v in base.items() if v is not None}, instance=user)

    def test_incomplete_profile_redirects_member_pages(self):
        user = make_user(complete=False)
        self.client.force_login(user)
        self.assertRedirects(self.client.get(reverse("items:mine")), reverse("accounts:profile"))
        self.assertRedirects(self.client.get(reverse("items:catalog")), reverse("accounts:profile"))
        self.assertEqual(self.client.get(reverse("accounts:privacy")).status_code, 200)

    def test_completing_profile(self):
        user = make_user(complete=False)
        self.client.force_login(user)
        response = self.client.post(
            reverse("accounts:profile"),
            {"pseudo": "Alice", "neighborhood": self.neighborhood.pk, "share_email": "on", "accept_terms": "on"},
        )
        self.assertRedirects(response, reverse("items:catalog"))
        user.refresh_from_db()
        self.assertTrue(user.is_profile_complete)

    def test_terms_must_be_accepted(self):
        form = self.form(make_user(complete=False))
        self.assertFalse(form.is_valid())
        self.assertIn("accept_terms", form.errors)

    def test_pseudo_is_unique_case_insensitive(self):
        make_user(pseudo="Alice")
        form = self.form(make_user(), pseudo="aLiCe")
        self.assertFalse(form.is_valid())
        self.assertIn("pseudo", form.errors)

    def test_pseudo_length(self):
        self.assertIn("pseudo", self.form(make_user(), pseudo="ab").errors)

    def test_at_least_one_channel(self):
        form = self.form(make_user(), share_email=None)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_sharing_phone_requires_phone(self):
        form = self.form(make_user(), share_email=None, share_phone="on")
        self.assertIn("share_phone", form.errors)

    def test_removing_only_shared_phone_is_refused(self):
        user = make_user(phone="0600000000", share_email=False, share_phone=True)
        form = self.form(user, share_email=None, share_phone="on", phone="")
        self.assertFalse(form.is_valid())

    def test_invalid_phone(self):
        self.assertIn("phone", self.form(make_user(), phone="abc").errors)
        self.assertTrue(self.form(make_user(), phone="06 12 34 56 78").is_valid())

    def test_inactive_neighborhood_not_offered(self):
        inactive = make_neighborhood(is_active=False)
        form = self.form(make_user(), neighborhood=inactive.pk)
        self.assertIn("neighborhood", form.errors)

    def test_logout(self):
        self.client.force_login(make_user())
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("items:catalog"))
        self.assertNotIn("_auth_user_id", self.client.session)


class DeleteAccountTests(TestCase):
    def test_delete_account(self):
        user = make_user(email="gone@example.com", pseudo="Partant", phone="0600000000", share_phone=True)
        item = make_item(owner=user)
        other = make_user()
        other_item = make_item(owner=other)
        received = send_request(other, item)
        sent = send_request(user, other_item)

        self.client.force_login(user)
        response = self.client.post(reverse("accounts:delete"))
        self.assertRedirects(response, reverse("items:catalog"))

        user.refresh_from_db()
        self.assertFalse(user.is_active)
        self.assertIsNone(user.pseudo)
        self.assertEqual(user.phone, "")
        self.assertNotIn("gone@example.com", user.email)
        self.assertEqual(user.display_name, "Utilisateur supprimé")
        self.assertFalse(Item.objects.available().filter(pk=item.pk).exists())
        received.refresh_from_db()
        sent.refresh_from_db()
        self.assertEqual(received.status, ContactRequest.Status.CANCELLED)
        self.assertEqual(sent.status, ContactRequest.Status.CANCELLED)
        self.assertEqual(sent.requester_email, "")

        # L'historique de l'autre membre affiche « Utilisateur supprimé ».
        self.client.force_login(other)
        self.assertContains(self.client.get(reverse("contacts:received")), "Utilisateur supprimé")

    def test_same_email_can_sign_up_again(self):
        user = make_user(email="gone@example.com")
        delete_account(user)
        cache.clear()
        self.client.post(reverse("accounts:login"), {"email": "gone@example.com"})
        new_user = User.objects.get(email="gone@example.com")
        self.assertNotEqual(new_user.pk, user.pk)


class LegalPagesTests(TestCase):
    def test_accessible_anonymously(self):
        for name in ["accounts:legal", "accounts:privacy"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)


class PurgeUnusedAccountsTests(TestCase):
    def test_purges_only_old_never_used_accounts(self):
        old = User.objects.create_user("old@example.com", date_joined=timezone.now() - timezone.timedelta(days=8))
        recent = User.objects.create_user("recent@example.com")
        member = make_user(date_joined=timezone.now() - timezone.timedelta(days=30))
        call_command("purge_unused_accounts", stdout=mock.MagicMock())
        self.assertFalse(User.objects.filter(pk=old.pk).exists())
        self.assertTrue(User.objects.filter(pk=recent.pk).exists())
        self.assertTrue(User.objects.filter(pk=member.pk).exists())


class DemoDataTests(TestCase):
    @override_settings(DEBUG=True)
    def test_load_demo_data_is_idempotent(self):
        call_command("load_demo_data", stdout=mock.MagicMock())
        call_command("load_demo_data", stdout=mock.MagicMock())
        self.assertEqual(Neighborhood.objects.count(), 5)
        self.assertEqual(Item.objects.available().count(), 5)

    def test_refused_without_debug(self):
        with self.assertRaises(CommandError):
            call_command("load_demo_data", stdout=mock.MagicMock())


class NoNeighborhoodTests(TestCase):
    def test_profile_explains_missing_neighborhoods(self):
        self.client.force_login(make_user(complete=False, is_staff=True))
        response = self.client.get(reverse("accounts:profile"))
        self.assertContains(response, "Aucun quartier n'est encore disponible")
        self.assertContains(response, reverse("admin:accounts_neighborhood_changelist"))
