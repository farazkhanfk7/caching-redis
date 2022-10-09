from django.contrib import admin
from django.urls import path
from .views import BookView, BookDetailView,func

urlpatterns = [
    path('book/', BookView.as_view(), name="book"),
    path('book/<str:name>/', BookDetailView.as_view(), name="book-detail"),
    path('book2/', func, name="book2"),
]