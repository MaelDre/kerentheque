from django.core import mail
from django.test import TestCase
from django.urls import reverse

from accounts.factories import make_user


class FeedbackTests(TestCase):
    def setUp(self):
        self.user = make_user(email="membre@example.com")

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse("feedback:send"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_send_feedback(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("feedback:send"), {"message": "Une super idée"})
        self.assertRedirects(response, reverse("items:catalog"))

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, ["noreply@localhost"])
        self.assertEqual(email.reply_to, ["membre@example.com"])
        self.assertIn("Une super idée", email.body)
        self.assertIn("membre@example.com", email.body)

    def test_empty_message_rejected(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("feedback:send"), {"message": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Écrivez un message")
        self.assertEqual(len(mail.outbox), 0)
