from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200)
    phone  = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
