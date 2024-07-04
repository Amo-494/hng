from django.urls import path
from api import views

# api/urls.py

urlpatterns = [
    path('hng', views.hng_view, name='hng'),
]