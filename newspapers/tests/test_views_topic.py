from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspapers.models import Topic

TOPIC_URL = reverse("newspapers:topic-list")
NEWSPAPER_URL = reverse("newspapers:newspaper-list")
REDACTOR_URL = reverse("newspapers:redactor-list")


class PublicTopicTest(TestCase):
    def test_login_required(self):
        """
        We check that a non-logged-in user does not have access to the topic list.
        :return:
        """
        res = self.client.get(TOPIC_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTopicTest(TestCase):
    def setUp(self) -> None:
        """
        We set up the test user and log him in before each test.
        :return:
        """
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_topic(self):
        """
        We check that the logged-in user can get the list of topics.
        :return:
        """
        Topic.objects.create(name="test_topic")
        response = self.client.get(TOPIC_URL)
        self.assertEqual(response.status_code, 200)
        topics = Topic.objects.all()
        self.assertEqual(
            list(response.context["topic_list"]),
            list(topics),
        )
        self.assertTemplateUsed(response, "newspapers/topic_list.html")


class TopicListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
        )
        self.client.force_login(self.user)

    def test_search_topic_without_filter(self) -> None:
        """
        We check that if there are no filters, the entire list of topics is returned.
        :return:
        """
        Topic.objects.create(name="test_topic")
        res = self.client.get(TOPIC_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["topic_list"]), list(Topic.objects.all()))
        self.assertTemplateUsed(res, "newspapers/topic_list.html")

    def test_search_topic_with_filter(self) -> None:
        """

         We check that the search by partial matching of the topic name works correctly.
        :return:
        """
        Topic.objects.create(name="test_topic")
        url = TOPIC_URL + "?name=test_topic"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["topic_list"]),
            list(Topic.objects.filter(name__icontains="test_to")),
        )
        self.assertTemplateUsed(res, "newspapers/topic_list.html")


class TopicUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="Politics")

    def test_update_topic_get(self) -> None:
        """
        Checking if the update page opens
        :return:
        """
        url = reverse("newspapers:topic-update", args=[self.topic.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "newspapers/topic_form.html")

    def test_update_topic_post(self) -> None:
        """
        We check whether the data is updated
        :return:
        """
        url = reverse("newspapers:topic-update", args=[self.topic.id])
        res = self.client.post(url, {"name": "Update Topic"})
        self.topic.refresh_from_db()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.topic.name, "Update Topic")
