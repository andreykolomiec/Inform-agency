from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from newspapers.models import Redactor

TOPIC_URL = reverse("newspapers:topic-list")
NEWSPAPER_URL = reverse("newspapers:newspaper-list")
REDACTOR_URL = reverse("newspapers:redactor-list")


class PublicRedactorTest(TestCase):
    def test_login_required(self) -> None:
        """
        Checks whether access to the editors page requires authentication.
        If the user is not authorized, the response status code should not be 200.
        :return:
        """
        res = self.client.get(REDACTOR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateRedactorTest(TestCase):
    def setUp(self) -> None:
        """
        Creates a user for testing with authorization.
        :return:
        """
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_redactor(self) -> None:
        """
        Checks that the editor is created correctly via the form.
        :return:
        """
        get_user_model().objects.create_user(username="test_redactor")
        response = self.client.get(REDACTOR_URL)
        self.assertEqual(response.status_code, 200)
        redactors = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["redactor_list"]),
            list(redactors),
        )
        self.assertTemplateUsed(response, "newspapers/redactor_list.html")

    def test_create_redactor(self) -> None:
        """
         Checks that the new editor is created correctly via the form.
         The test checks whether the editor's data (name, surname, work experience) are stored correctly
         after sending a POST request.
        :return:
        """
        form_date = {
            "username": "test_redactor",
            "password1": "Redactor12!@#",
            "password2": "Redactor12!@#",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": 5,
        }
        response = self.client.post(
            reverse("newspapers:redactor-create"), data=form_date
        )
        if response.context and "form" in response.context:
            print(response.context["form"].errors)
        new_redactor = get_user_model().objects.get(username=form_date["username"])

        self.assertEqual(new_redactor.first_name, form_date["first_name"])
        self.assertEqual(new_redactor.last_name, form_date["last_name"])
        self.assertEqual(
            new_redactor.years_of_experience, form_date["years_of_experience"]
        )


class RedactorListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test123", years_of_experience=5
        )
        self.client.force_login(self.user)

    def test_search_redactor_without_filter(self) -> None:
        """
        Checks whether all redactors are displayed on the page without filtering.
        :return:
        """
        Redactor.objects.create_user(
            username="test_redactor",
            years_of_experience=5,
            first_name="test_first_name",
            last_name="test_last_name",
        )
        res = self.client.get(REDACTOR_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["redactor_list"]), list(Redactor.objects.all())
        )
        self.assertTemplateUsed(res, "newspapers/redactor_list.html")

    def test_search_redactor_with_filter(self) -> None:
        """
        Checks if filtering by username works correctly.
        :return:
        """
        Redactor.objects.create_user(
            username="test_redactor",
            years_of_experience=5,
            first_name="test_first_name",
            last_name="test_last_name",
        )
        url = REDACTOR_URL + "?username=test_redactor"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["redactor_list"]),
            list(Redactor.objects.filter(username__icontains="test_red")),
        )
        self.assertTemplateUsed(res, "newspapers/redactor_list.html")


class RedactorDetailViewTest(TestCase):
    def setUp(self) -> None:
        """
        Creates a user for testing and redactor to be accessed later.
        :return:
        """
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
            years_of_experience=5,
        )
        self.redactor = get_user_model().objects.create_user(
            username="test_redactor",
            password="test123",
            years_of_experience=5,
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.client.force_login(self.user)

    def test_retrieve_redactor_detail(self) -> None:
        """
        Checks whether the redactor details are displayed correctly on the page.
        :return:
        """
        url = reverse("newspapers:redactor-detail", args=[self.redactor.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["redactor"], self.redactor)
        self.assertTemplateUsed(res, "newspapers/redactor_detail.html")


class RedactorUpdateViewTest(TestCase):
    def setUp(self) -> None:
        """
        Створює користувача та редактора для тестування оновлення редактора.
        :return:
        """
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.redactor = get_user_model().objects.create_user(
            username="test_redactor",
            password="test123",
            years_of_experience=5,
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.client.force_login(self.user)

    def test_update_redactor_post(self) -> None:
        """
        checks if updating editor data via POST request works correctly.
        :return:
        """
        url = reverse("newspapers:redactor-update", args=[self.redactor.id])
        res = self.client.post(
            url,
            data={
                "username": "test_redactor",
                "first_name": "update_first_name",
                "last_name": "test_last_name",
                "years_of_experience": 5,
            },
        )
        if res.status_code == 200 and res.context:
            print(res.context["form"].errors)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse_lazy("newspapers:redactor-list"))
        self.redactor.refresh_from_db()
        self.assertEqual(self.redactor.first_name, "update_first_name")
