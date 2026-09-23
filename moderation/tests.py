from django.test import TestCase
from django.urls import reverse
from sesame.utils import get_query_string

from accounts.factories import make_item, make_user
from contacts.models import ContactRequest
from contacts.services import send_request
from items.models import Item

from .models import Report


class ReportTests(TestCase):
    def setUp(self):
        self.owner = make_user()
        self.item = make_item(owner=self.owner)
        self.member = make_user()
        self.client.force_login(self.member)

    def test_report_item(self):
        response = self.client.post(
            reverse("moderation:report", args=[self.item.pk]), {"target": "item", "reason": "Objet interdit"}
        )
        self.assertRedirects(response, self.item.get_absolute_url())
        report = Report.objects.get()
        self.assertEqual(report.item, self.item)
        self.assertEqual(report.author, self.member)

    def test_report_owner(self):
        self.client.post(reverse("moderation:report", args=[self.item.pk]), {"target": "user", "reason": "Spam"})
        self.assertEqual(Report.objects.get().user, self.owner)

    def test_reason_required(self):
        response = self.client.post(reverse("moderation:report", args=[self.item.pk]), {"target": "item", "reason": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Report.objects.exists())

    def test_cannot_report_own_item(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("moderation:report", args=[self.item.pk]), {"target": "item", "reason": "x"})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Report.objects.exists())


class AdminModerationTests(TestCase):
    def setUp(self):
        self.admin = make_user(is_staff=True, is_superuser=True)
        self.owner = make_user()
        self.item = make_item(owner=self.owner)
        self.requester = make_user()
        self.client.force_login(self.admin)

    def admin_action(self, model_url, action, pks):
        return self.client.post(
            reverse(model_url), {"action": action, "_selected_action": [str(pk) for pk in pks]}
        )

    def test_member_cannot_access_admin(self):
        self.client.force_login(self.requester)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)

    def test_suspend_and_reactivate_user(self):
        received = send_request(self.requester, self.item)
        self.admin_action("admin:accounts_user_changelist", "suspend", [self.owner.pk])
        self.owner.refresh_from_db()
        received.refresh_from_db()
        self.assertFalse(self.owner.is_active)
        self.assertEqual(received.status, ContactRequest.Status.CANCELLED)
        self.assertFalse(Item.objects.available().filter(pk=self.item.pk).exists())

        self.client.logout()
        token = get_query_string(self.owner).split("sesame=")[1]
        self.assertEqual(self.client.post(reverse("accounts:magic_link"), {"sesame": token}).status_code, 400)

        self.client.force_login(self.admin)
        self.admin_action("admin:accounts_user_changelist", "reactivate", [self.owner.pk])
        self.owner.refresh_from_db()
        self.assertTrue(self.owner.is_active)
        self.assertTrue(Item.objects.available().filter(pk=self.item.pk).exists())

    def test_remove_item(self):
        req = send_request(self.requester, self.item)
        self.admin_action("admin:items_item_changelist", "remove_items", [self.item.pk])
        self.item.refresh_from_db()
        req.refresh_from_db()
        self.assertIsNotNone(self.item.deleted_at)
        self.assertEqual(req.status, ContactRequest.Status.CANCELLED)

    def test_bulk_delete_disabled(self):
        response = self.admin_action("admin:items_item_changelist", "delete_selected", [self.item.pk])
        self.assertTrue(Item.objects.filter(pk=self.item.pk).exists())
        self.assertIn(response.status_code, (200, 302))

    def test_reports_list_and_mark_handled(self):
        report = Report.objects.create(author=self.requester, item=self.item, reason="Suspect")
        response = self.client.get(reverse("admin:moderation_report_changelist"))
        self.assertRedirects(response, reverse("admin:moderation_report_changelist") + "?handled=no")
        response = self.client.get(reverse("admin:moderation_report_changelist") + "?handled=no")
        self.assertContains(response, "Suspect")
        self.admin_action("admin:moderation_report_changelist", "mark_handled", [report.pk])
        report.refresh_from_db()
        self.assertIsNotNone(report.handled_at)

    def test_admin_pages_render(self):
        for name in [
            "admin:accounts_user_changelist",
            "admin:accounts_neighborhood_changelist",
            "admin:items_category_changelist",
            "admin:items_item_changelist",
            "admin:contacts_contactrequest_changelist",
        ]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)
        self.assertEqual(self.client.get(reverse("admin:accounts_user_change", args=[self.owner.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin:items_item_change", args=[self.item.pk])).status_code, 200)
