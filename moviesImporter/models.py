from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Movie(models.Model):
    imdb_id = models.CharField(max_length=255)
    title = models.CharField(validators=[MinLengthValidator(1)], max_length=255)
    genre_1 = models.CharField(max_length=255, null=True)
    genre_2 = models.CharField(max_length=255, null=True)
    genre_3 = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    director_1 = models.CharField(max_length=255, null=True)
    director_2 = models.CharField(max_length=255, null=True)
    director_3 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title