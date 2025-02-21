from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from newspapers.forms import (
    RedactorCreationForm,
    RedactorSearchForm,
    NewspaperForm,
    NewspaperSearchForm,
    TopicSearchForm,
)
from newspapers.models import Newspaper, Topic, Redactor


class RedactorCreationFormTest(TestCase):
    def test_redactor_creation_form_with_first_name_last_name_years_of_experience_is_valid(
        self,
    ) -> None:
        """
        check whether the data for the editor creation form is correctly processed and validated.
        :return:
        """
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first name",
            "last_name": "Test last name",
            "years_of_experience": 5,
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class RedactorSearchFormTest(TestCase):
    def test_redactor_creation_form_when_username_is_empty_is_valid(self) -> None:
        """
        The test checks if the form remains valid when the "username" field is empty
        :return:
        """
        form = RedactorSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_redactor_placeholder_in_widget(self) -> None:
        """
        The test checks whether the prompt text (placeholder) for the "username" field is correctly set
        :return:
        """
        form = RedactorSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"], "Search by username"
        )


class NewspaperCreationFormTest(TestCase):
    def setUp(self) -> None:
        """
        Create a new user to log in to the test session
        :return:
        """
        self.username = get_user_model().objects.create_user(
            username="new_user", password="user12test"
        )
        self.client.force_login(self.username)

    def test_newspaper_creation_form_with_publishers(self) -> None:
        """
        The test checks whether the form for creating a newspaper works with the correct fields,
        including the connection to the topic and publishers
        :return:
        """
        topic = Topic.objects.create(name="test_topic")
        newspaper = Newspaper.objects.create(
            title="test_newspaper",
            content="test_content",
            published_date=timezone.now().date(),
            topic=topic,
        )
        publisher = Redactor.objects.create_user(
            username="test_redactor",
        )
        newspaper.publishers.set([publisher])
        form_data = {
            "title": "test_newspaper",
            "content": "test_content",
            "published_date": timezone.now().date(),
            "topic": topic.id,
            "publishers": [publisher.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())

        cleaned_data = form.cleaned_data
        self.assertEqual(cleaned_data["title"], form_data["title"])
        self.assertEqual(cleaned_data["content"], form_data["content"])
        self.assertEqual(cleaned_data["published_date"], form_data["published_date"])
        self.assertEqual(cleaned_data["topic"].id, form_data["topic"])
        self.assertEqual(
            [publisher.id], [redactor.id for redactor in cleaned_data["publishers"]]
        )

    def test_newspaper_creation_form_publishers_is_empty_is_valid(self) -> None:
        """
        Checking that the publishers field can be empty
        :return:
        """
        topic = Topic.objects.create(name="test_topic")
        form_data = {
            "title": "test_newspaper",
            "content": "test_content",
            "published_date": "2025-02-04",
            "topic": topic.id,
            "publishers": [],
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_creation_form_invalid_without_title(self) -> None:
        """
        Checking that the form is not valid if the title field is not filled:
        :return:
        """
        topic = Topic.objects.create(name="test_topic")
        form_data = {
            "content": "test_content",
            "published_date": "2025-02-04",
            "topic": topic.id,
            "publishers": [1],
        }
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_newspaper_creation_form_multiple_publishers_is_valid(self) -> None:
        """
        Verifying that the publishers field works correctly with multiple values
        :return:
        """
        username1 = get_user_model().objects.create_user(
            username="new_user1", password="user12test"
        )
        username2 = get_user_model().objects.create_user(
            username="new_user2", password="user13test"
        )
        topic = Topic.objects.create(name="test_topic")
        form_data = {
            "title": "test_newspaper",
            "content": "test_content",
            "published_date": "2025-02-04",
            "topic": topic.id,
            "publishers": [username1.id, username2.id],
        }

        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())


class NewspaperSearchFormTest(TestCase):
    def setUp(self) -> None:
        self.username = get_user_model().objects.create_user(
            username="new_user", password="test12test"
        )
        self.client.force_login(self.username)

    def test_newspaper_creation_form_empty_topic(self) -> None:
        """
        validates the form when the topic field is left blank or set to None
        :return:
        """
        form_data = {
            "title": "test_newspaper",
            "content": "test_content",
            "published_date": "2025-02-04",
            "topic": None,
            "publishers": [self.username.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_search_form_with_topic(self) -> None:
        """
        Checks that newspapers are filtered correctly
        by topic name if case-insensitive partial match search is provided .
        :return:
        """
        topic1 = Topic.objects.create(name="Test topic")
        topic2 = Topic.objects.create(name="Other topic")
        newspaper1 = Newspaper.objects.create(
            title="Test Newspaper",
            content="test_content",
            published_date="2025-02-04",
            topic=topic1,
        )
        newspaper2 = Newspaper.objects.create(
            title="Other Newspaper2",
            content="other_content",
            published_date="2025-02-04",
            topic=topic2,
        )
        form_data = {"topic": "test"}
        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = form.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertIn(newspaper1, queryset)
        self.assertNotIn(newspaper2, queryset)

    def test_newspaper_search_form_no_result(self) -> None:
        """
        Checking that a form with an input value that does not exist in the topic does not find any records
        :return:
        """
        form_data = {"topic": "Nonexistent Topic "}
        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = form.get_queryset()
        self.assertEqual(queryset.count(), 0)


class TopicSearchFormTest(TestCase):
    def setUp(self) -> None:
        self.username = get_user_model().objects.create_user(
            username="new_user",
        )
        self.client.force_login(self.username)

    def test_topic_search_form_when_name_empty_is_valid(self) -> None:
        """
        Validating the form even if the "name" field is empty.
        :return:
        """
        form_data = {
            "name": "",
        }
        form = TopicSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_topic_search_form_with_name_is_valid(self) -> None:
        """
        Checks that topics are filtered correctly
        by name if case-insensitive partial match search is provided .
        :return:
        """
        topic1 = Topic.objects.create(name="Test topic")
        topic2 = Topic.objects.create(name="Other topic")
        form_data = {"name": "test"}
        form = TopicSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = form.get_queryset()
        print(queryset.count(), queryset.values_list("name", flat=True))
        self.assertEqual(queryset.count(), 1)
        self.assertIn(topic1, queryset)
        self.assertNotIn(topic2, queryset)

    def test_topic_search_form_placeholder_in_widget(self) -> None:
        """
        This test checks that the placeholder for the 'name' field in the form is correctly set
        :return:
        """
        form = TopicSearchForm()
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], "Search by name"
        )
