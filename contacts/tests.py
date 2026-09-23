from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.factories import make_item, make_user

from . import services
from .models import ContactRequest

Status = ContactRequest.Status


class ContactRequestFlowTests(TestCase):
    def setUp(self):
        self.owner = make_user(pseudo="Proprio", email="owner@example.com", phone="0611111111", share_phone=True)
        self.requester = make_user(pseudo="Demandeur", email="req@example.com", phone="0622222222")
        self.item = make_item(owner=self.owner, name="Tente 4 places")

    def send(self, user=None, **data):
        self.client.force_login(user or self.requester)
        payload = {"message": "Pour ce week-end", "consent": "on"}
        payload.update(data)
        return self.client.post(reverse("contacts:send", args=[self.item.pk]), {k: v for k, v in payload.items() if v is not None})

    def test_full_cycle_accept(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.send()
        self.assertRedirects(response, reverse("contacts:sent"))
        req = ContactRequest.objects.get()
        self.assertEqual(req.status, Status.PENDING)
        self.assertEqual(req.requester_email, "req@example.com")
        self.assertEqual(req.requester_phone, "")  # le demandeur ne partage pas son téléphone

        # Email au propriétaire avec les coordonnées du demandeur et le message.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["owner@example.com"])
        self.assertIn("req@example.com", mail.outbox[0].body)
        self.assertIn("Pour ce week-end", mail.outbox[0].body)
        self.assertIn("/demandes-recues/", mail.outbox[0].body)

        # Le propriétaire voit la demande et les coordonnées transmises.
        self.client.force_login(self.owner)
        self.assertContains(self.client.get(reverse("contacts:received")), "req@example.com")

        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(reverse("contacts:accept", args=[req.pk]))
        req.refresh_from_db()
        self.assertEqual(req.status, Status.ACCEPTED)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].to, ["req@example.com"])
        self.assertIn("owner@example.com", mail.outbox[1].body)
        self.assertIn("0611111111", mail.outbox[1].body)

        self.client.force_login(self.requester)
        response = self.client.get(reverse("contacts:sent"))
        self.assertContains(response, "Acceptée")
        self.assertContains(response, "0611111111")

    def test_refuse_sends_no_email(self):
        req = services.send_request(self.requester, self.item)
        mail.outbox.clear()
        self.client.force_login(self.owner)
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(reverse("contacts:refuse", args=[req.pk]))
        req.refresh_from_db()
        self.assertEqual(req.status, Status.REFUSED)
        self.assertEqual(mail.outbox, [])
        self.client.force_login(self.requester)
        self.assertContains(self.client.get(reverse("contacts:sent")), "Refusée")

    def test_consent_required(self):
        response = self.send(consent=None)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "accepter la transmission")
        self.assertFalse(ContactRequest.objects.exists())

    def test_cannot_request_own_item(self):
        self.send(user=self.owner)
        self.assertFalse(ContactRequest.objects.exists())

    def test_cannot_request_unavailable_item(self):
        self.item.deleted_at = self.item.created_at
        self.item.save()
        self.assertEqual(self.send().status_code, 404)

    def test_no_duplicate_even_after_refusal(self):
        req = services.send_request(self.requester, self.item)
        services.refuse(req, self.owner)
        self.send()
        self.assertEqual(ContactRequest.objects.count(), 1)
        response = self.client.get(self.item.get_absolute_url())
        self.assertNotContains(response, "Envoyer ma demande")
        self.assertContains(response, "Refusée")

    @override_settings(MAX_PENDING_REQUESTS=5)
    def test_pending_limit(self):
        for i in range(5):
            services.send_request(self.requester, make_item(name=f"Objet {i}"))
        with self.assertRaises(services.RequestError):
            services.send_request(self.requester, self.item)
        response = self.send()
        self.assertEqual(ContactRequest.objects.filter(item=self.item).count(), 0)
        self.assertRedirects(response, self.item.get_absolute_url())

    def test_decision_is_final(self):
        req = services.send_request(self.requester, self.item)
        services.refuse(req, self.owner)
        with self.assertRaises(services.RequestError):
            services.accept(req, self.owner)
        req.refresh_from_db()
        self.assertEqual(req.status, Status.REFUSED)

    def test_cancelled_request_cannot_be_accepted(self):
        req = services.send_request(self.requester, self.item)
        services.cancel_pending_for_item(self.item)
        with self.assertRaises(services.RequestError):
            services.accept(req, self.owner)

    def test_third_party_cannot_decide(self):
        req = services.send_request(self.requester, self.item)
        self.client.force_login(make_user())
        self.assertEqual(self.client.post(reverse("contacts:accept", args=[req.pk])).status_code, 404)
        with self.assertRaises(services.RequestError):
            services.accept(req, make_user())
        req.refresh_from_db()
        self.assertEqual(req.status, Status.PENDING)

    def test_contact_details_frozen_at_transmission(self):
        req = services.send_request(self.requester, self.item)
        self.requester.share_phone = True
        self.requester.save()
        self.client.force_login(self.owner)
        response = self.client.get(reverse("contacts:received"))
        self.assertContains(response, "req@example.com")
        self.assertNotContains(response, "0622222222")

        services.accept(req, self.owner)
        self.owner.share_email = False
        self.owner.save()
        req.refresh_from_db()
        self.assertEqual(req.owner_email, "owner@example.com")

    def test_only_shared_channels_transmitted_on_accept(self):
        self.owner.share_phone = False
        self.owner.save()
        req = services.send_request(self.requester, self.item)
        services.accept(req, self.owner)
        req.refresh_from_db()
        self.assertEqual(req.owner_phone, "")

    def test_received_lists_pending_first(self):
        old = services.send_request(self.requester, self.item)
        services.refuse(old, self.owner)
        other_item = make_item(owner=self.owner, name="Barbecue")
        services.send_request(make_user(), other_item)
        self.client.force_login(self.owner)
        content = self.client.get(reverse("contacts:received")).content.decode()
        self.assertLess(content.index("Barbecue"), content.index("Tente 4 places"))

    def test_member_pages_require_login(self):
        for name in ["contacts:sent", "contacts:received"]:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse("accounts:login"), response.url)
