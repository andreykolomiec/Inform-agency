from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from newspapers.models import Topic, Newspaper


class ModelTests(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEqual(str(topic), topic.name)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create(
            username="redactor",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username}:"
            f" ({redactor.first_name}"
            f" {redactor.last_name})",
        )

    def test_newspaper_str(self):
        topic = Topic.objects.create(name="test")
        redactor = get_user_model().objects.create(
            username="redactor",
        )
        newspaper = Newspaper.objects.create(
            title="Test", topic=topic, published_date="2025-01-31"
        )
        newspaper.publishers.add(redactor)
        self.assertEqual(
            str(newspaper),
            f"{newspaper.title}: ("
            f"topic: {newspaper.topic},"
            f" publishers: {newspaper.publishers},"
            f" published_date: {newspaper.published_date}"
            f")",
        )

    def test_create_redactor_with_years_of_experience(self):
        username = "redactor"
        password = "test123"
        years_of_experience = 5
        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience,
        )
        self.assertEqual(redactor.username, username)
        self.assertEqual(redactor.years_of_experience, years_of_experience)
        self.assertTrue(redactor.check_password(password))

    def test_get_redactor_absolute_url(self):
        redactor = get_user_model().objects.create_user(
            username="redactor",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        expected_url = f"/newspapers/redactors/{redactor.id}/"
        self.assertEqual(redactor.get_absolute_url(), expected_url)

    def test_get_newspaper_absolute_url(self):
        topic = Topic.objects.create(name="topic")
        redactor = get_user_model().objects.create_user(
            username="redactor",
        )
        newspaper = Newspaper.objects.create(
            title="Test",
            topic=topic,
            published_date=timezone.now(),
        )
        newspaper.publishers.add(redactor)
        expected_url = f"/newspapers/newspapers/{newspaper.id}/"
        self.assertEqual(newspaper.get_absolute_url(), expected_url)
