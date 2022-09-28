from django.contrib import admin
from django.urls import path
from .views import BookView

urlpatterns = [
    path('book/', BookView.as_view(), name="book"),
]