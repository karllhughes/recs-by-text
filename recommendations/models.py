from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ObjectDoesNotExist
from moviesImporter.models import Movie


class User(models.Model):
    username = models.CharField(validators=[MinLengthValidator(3)], max_length=200, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def does_trust(self, another_user):
        try:
            return bool(TrustedUser.objects.get(original_user=self, trusted_user=another_user))
        except ObjectDoesNotExist as e:
            return False

    def is_trusted_by(self, another_user):
        try:
            return bool(TrustedUser.objects.get(original_user=another_user, trusted_user=self))
        except ObjectDoesNotExist as e:
            return False


class Recommendation(models.Model):
    recommender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='recommendations_made')
    recommendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations_recieved')
    name = models.CharField(validators=[MinLengthValidator(1)], max_length=255)
    context = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    movie = models.ForeignKey(Movie, blank=True, null=True, on_delete=models.SET_NULL, related_name='movie')

    def __str__(self):
        return self.name


class TrustedUser(models.Model):
    original_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    trusted_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trusted_user')
    created_at = models.DateTimeField(auto_now_add=True)


from .signals import recommendation_pre_save  # noqa
