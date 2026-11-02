from django.test import TestCase
from django.urls import reverse

from accounts.factories import make_item, make_user

PROJECT_LINK = f'href="{reverse("project")}"'
BANNER = 'class="project-banner"'


class ProjectPageTests(TestCase):
    def test_accessible_anonymously(self):
        response = self.client.get("/le-projet/")
        self.assertEqual(response.status_code, 200)

    def test_accessible_when_logged_in(self):
        self.client.force_login(make_user())
        response = self.client.get(reverse("project"))
        self.assertContains(response, "Mon compte")

    def test_sections_in_order(self):
        content = self.client.get(reverse("project")).content.decode()
        titles = ["Pourquoi ?", "Comment ça marche ?", "Qui sommes-nous ?", "Les prochaines étapes"]
        positions = [content.index(f"<h2>{title}</h2>") for title in titles]
        self.assertEqual(positions, sorted(positions))


class ProjectLinksTests(TestCase):
    def assert_header_and_footer_links(self):
        content = self.client.get(reverse("accounts:legal")).content.decode()
        header = content.split("</header>")[0]
        footer = content.split("<footer")[1]
        self.assertIn(PROJECT_LINK, header)
        self.assertIn(PROJECT_LINK, footer)

    def test_links_for_anonymous_visitor(self):
        self.assert_header_and_footer_links()

    def test_links_for_member_outside_account_menu(self):
        self.client.force_login(make_user())
        self.assert_header_and_footer_links()
        content = self.client.get(reverse("accounts:legal")).content.decode()
        account_menu = content.split('<details class="dropdown">')[1].split("</details>")[0]
        self.assertNotIn(PROJECT_LINK, account_menu)


class ProjectBannerTests(TestCase):
    def test_banner_on_home_for_everyone(self):
        for user in [None, make_user()]:
            if user:
                self.client.force_login(user)
            response = self.client.get(reverse("items:catalog"))
            self.assertContains(response, BANNER)
            banner = response.content.decode().split(BANNER)[1].split("</aside>")[0]
            self.assertIn(PROJECT_LINK, banner)
            # Secondary action: "Filtrer" stays the only primary button on the page.
            self.assertIn('class="secondary"', banner)

    def test_no_banner_elsewhere(self):
        item = make_item()
        for url in [reverse("project"), item.get_absolute_url()]:
            self.assertNotContains(self.client.get(url), BANNER)
