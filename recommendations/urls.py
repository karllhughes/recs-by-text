from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('sms', views.sms, name='sms')
]