from django.urls import path
from .views import create_major

urlpatterns = [
    path('major/create/', create_major, name='create_major'),
] 