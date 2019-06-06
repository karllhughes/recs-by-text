from django.contrib import admin
from .models import User, Recommendation, TrustedUser 

admin.site.register(User)
admin.site.register(Recommendation)
admin.site.register(TrustedUser)

