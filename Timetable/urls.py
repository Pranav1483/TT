from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate, name='generate'),
    path('make/', views.make, name='make'),
]

