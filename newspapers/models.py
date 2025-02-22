from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.username}: ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("newspapers:redactor-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="newspapers"
    )

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return (
            f"{self.title}: ("
            f"topic: {self.topic},"
            f" publishers: {self.publishers},"
            f" published_date: {self.published_date}"
            f")"
        )

    def get_absolute_url(self):
        return reverse("newspapers:newspaper-detail", args=[str(self.id)])
