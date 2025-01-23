from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = ("years_of_experience",)

    def __str__(self):
        return (
            f"{self.years_of_experience} ("
            f"username:{self.username},"
            f" email:{self.email},"
            f" password:{self.password},"
            f" first_name:{self.first_name},"
            f" last_name:{self.last_name}"
            f")"
        )

class Newspaper(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="newspapers")
    publishers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="newspapers")

    class Meta:
        ordering = ("published_date",)

    def __str__(self):
        return self.title
