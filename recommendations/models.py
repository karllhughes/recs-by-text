from django.db import models
from django.core.validators import MinLengthValidator

class User(models.Model):
    username = models.CharField(validators=[MinLengthValidator(3)], max_length=200, unique=True)
    phone  = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Recommendation(models.Model):
    recommender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='recommendations_made')
    recommendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations_recieved')
    name = models.CharField(validators=[MinLengthValidator(1)], max_length=255)
    context = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class TrustedUser(models.Model): 
    original_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    trusted_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trusted_user')
    created_at = models.DateTimeField(auto_now_add=True)
    



    
