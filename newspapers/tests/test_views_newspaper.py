from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from newspapers.models import Topic, Newspaper, Redactor

TOPIC_URL = reverse("newspapers:topic-list")
NEWSPAPER_URL = reverse("newspapers:newspaper-list")
REDACTOR_URL = reverse("newspapers:redactor-list")


class PublicNewspaperTest(TestCase):
    def test_login_required(self) -> None:
        """
        Checks that access to the newspaper list requires authentication.
        An unauthorized user is expected to receive a status code other than 200.
        :return:
        """
        res = self.client.get(NEWSPAPER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateNewspaperTest(TestCase):
    def setUp(self) -> None:
        """
        Configures a test user and performs authorization
        :return:
        """
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_newspaper(self) -> None:
        """
        Checks that an authorized user can retrieve a list of newspapers.
        :return:
        """
        topic = Topic.objects.create(name="test_topic")
        newspaper = Newspaper.objects.create(
            title="test_newspaper",
            content="test_content",
            published_date=timezone.now(),
            topic=topic,
        )
        publisher = Redactor.objects.create(
            username="test_redactor",
        )
        newspaper.publishers.set([publisher])
        response = self.client.get(NEWSPAPER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["newspaper_list"]),
            list(Newspaper.objects.all()),
        )
        self.assertTemplateUsed(response, "newspapers/newspaper_list.html")


class NewspaperListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_search_newspaper_without_filter(self) -> None:
        """
        Checks that the list of newspapers is displayed correctly without applying filters.
        :return:
        """
        topic = Topic.objects.create(name="test_topic")
        newspaper = Newspaper.objects.create(
            title="test_newspaper",
            content="test_content",
            published_date=timezone.now(),
            topic=topic,
        )
        publisher = Redactor.objects.create(
            username="test_redactor",
        )
        newspaper.publishers.set([publisher])
        res = self.client.get(NEWSPAPER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["newspaper_list"]), list(Newspaper.objects.all())
        )
        self.assertTemplateUsed(res, "newspapers/newspaper_list.html")

    def test_search_newspaper_with_filter(self) -> None:
        """
        Checks that the list of newspapers is correctly filtered by part of the subject name.
        :return:
        """
        topic = Topic.objects.create(
            name="test_newspaper",
        )
        newspaper = Newspaper.objects.create(
            title="test_newspaper",
            content="test_content",
            published_date=timezone.now(),
            topic=topic,
        )
        publisher = Redactor.objects.create(
            username="test_redactor",
        )
        newspaper.publishers.set([publisher])
        url = NEWSPAPER_URL + "?name=test_news"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["newspaper_list"]),
            list(Newspaper.objects.filter(topic__name__icontains="test_news")),
        )
        self.assertTemplateUsed(res, "newspapers/newspaper_list.html")

    def test_retrieve_newspaper_detail(self) -> None:
        """
        Checks that the details page of a particular newspaper is displayed correctly.
        :return:
        """
        topic = Topic.objects.create(name="test_topic")
        newspaper = Newspaper.objects.create(
            title="test_newspaper",
            content="test_content",
            published_date=timezone.now(),
            topic=topic,
        )
        publisher = Redactor.objects.create(
            username="test_redactor",
        )
        newspaper.publishers.set([publisher])
        url = reverse("newspapers:newspaper-detail", args=[newspaper.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["newspaper"], newspaper)
        self.assertTemplateUsed(res, "newspapers/newspaper_detail.html")


class NewspaperUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_update_newspaper_view_get(self):
        """
        We check that the GET request to the newspaper editing form works correctly.
        :return:
        """
        topic = Topic.objects.create(name="test_topic")
        newspaper = Newspaper.objects.create(
            title="test_newspaper",
            content="test_content",
            published_date=timezone.now(),
            topic=topic,
        )
        publisher = Redactor.objects.create(
            username="test_redactor",
        )
        newspaper.publishers.set([publisher])
        url = reverse("newspapers:newspaper-update", args=[newspaper.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["newspaper"], newspaper)

    def test_update_newspaper_view_post(self):
        """
        Check that the POST request updates the newspaper data.
        :return:
        """
        topic = Topic.objects.create(name="test_topic")
        newspaper = Newspaper.objects.create(
            title="test_newspaper",
            content="test_content",
            published_date=timezone.now(),
            topic=topic,
        )
        publisher = Redactor.objects.create(
            username="test_redactor",
        )
        newspaper.publishers.set([publisher])
        url = reverse("newspapers:newspaper-update", args=[newspaper.id])
        res = self.client.post(
            url,
            data={
                "title": "Updated title",
                "content": "Updated content",
                "topic": topic.id,
                "published_date": newspaper.published_date.strftime("%Y-%m-%d"),
                "publishers": [publisher.id],
            },
        )
        newspaper.refresh_from_db()
        print(res.content.decode())
        self.assertEqual(newspaper.title, "Updated title")
        self.assertEqual(res.status_code, 302)
