from crispy_bootstrap5.bootstrap5 import FloatingField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from newspapers.models import Redactor, Newspaper, Topic


class RedactorCreationForm(UserCreationForm):
    """
    Redactor registration form with Bootstrap 5 support
    """

    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField("username"),
            FloatingField("first_name"),
            FloatingField("last_name"),
            FloatingField("years_of_experience"),
            FloatingField("password1"),
            FloatingField("password2"),
            Submit("submit", "Register", css_class="btn btn-primary w-100"),
        )


class RedactorSearchForm(forms.Form):
    """
    Search for redactors by username
    """

    username = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username",
                "class": "form-control",
            }
        ),
    )


class NewspaperForm(forms.ModelForm):
    """
    Form for creating a newspaper
    """

    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check"}),
        required=False,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField("title"),
            FloatingField("content"),
            FloatingField("topic"),
            "publishers",
            Submit("submit", "Save", css_class="btn btn-success w-100"),
        )


class NewspaperSearchForm(forms.Form):
    """
    Search for newspaper by topic
    """

    topic = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by topic",
                "class": "form-control",
            }
        ),
    )

    def get_queryset(self):
        queryset = Newspaper.objects.all()
        topic = self.cleaned_data.get("topic")
        if topic:
            queryset = queryset.filter(topic__name__icontains=topic)
        return queryset


class TopicSearchForm(forms.Form):
    """
    Search for topic by name
    """

    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
                "class": "form-control",
            }
        ),
    )

    def get_queryset(self):
        queryset = Topic.objects.all()
        topic = self.cleaned_data.get("name")
        if topic:
            queryset = queryset.filter(name__icontains=self.cleaned_data.get("name"))
        return queryset
