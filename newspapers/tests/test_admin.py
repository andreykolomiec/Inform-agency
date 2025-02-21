from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin",
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="redactor",
            password="test_redactor",
            first_name="redactor_first",
            last_name="redactor_last",
            years_of_experience=5,
        )

    def test_redactor_years_of_experience_listed(self):
        """
        Test that redactor's years_of_experience is in list_display on redactor admin page
        :return:
        """
        url = reverse("admin:newspapers_redactor_changelist")
        res = self.client.get(url)
        self.assertContains(res, "Years of experience")
        self.assertContains(res, str(self.redactor.years_of_experience))

    def test_redactor_detail_years_of_experience_listed(self):
        """
        Test that redactor's years_of_experience is on redactor detail admin page
        :return:
        """
        url = reverse("admin:newspapers_redactor_change", args=[self.redactor.id])
        res = self.client.get(url)
        self.assertContains(res, "Years of experience")
        self.assertContains(res, str(self.redactor.years_of_experience))

    def test_redactor_add_full_name_years_of_experience_listed(self):
        """
        Test that redactor's first_name, last_name and years_of_experience is on redactor add admin page
        :return:
        """
        url = reverse("admin:newspapers_redactor_add")
        res = self.client.get(url)
        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")
        self.assertContains(res, "5")
        self.assertContains(res, str(self.redactor.years_of_experience))
