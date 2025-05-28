from django.contrib.auth import get_user_model
from django.db import models

from Petstagram.photos.models import Photo


# Create your models here.

UserModel = get_user_model()


class Comment(models.Model):
    text = models.TextField(
        max_length=300,
    )

    date_time_of_publication = models.DateTimeField(
        auto_now_add=True,
    )

    to_photo = models.ForeignKey(
        to=Photo,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        indexes = [
            models.Index(fields=['date_time_of_publication'])
        ]
        ordering = ['-date_time_of_publication']


class Like(models.Model):
    to_photo = models.ForeignKey(
        to=Photo,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )
