from rest_framework.views import APIView
from .models import Book
from .serializer import BookSerializer
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
from rest_framework.decorators import permission_classes, api_view
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import logging


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.
@permission_classes((permissions.AllowAny,))
class BookView(APIView):

    def get_queryset(self, name=None):
        queryset = Book.objects.all()
        return queryset
    
    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class BookDetailView(APIView):

    def get_object(self, name=None):
        queryset = Book.objects.get(name=name)
        return queryset
    
    def get(self, request, name, format=None):
        if cache.get(name):
            # If the data is in the cache, return it.
            print("Cache hit")
            return Response(cache.get(name))
        # If the data is not in the cache, get it from the database.
        print("Cache miss")
        queryset = self.get_object(name)
        serializer = BookSerializer(queryset)
        # Setting Cache
        cache.set(name, serializer.data, timeout=CACHE_TTL)
        return Response(serializer.data)

    def put(self, request, name, format=None):
        queryset = self.get_object(name)
        serializer = BookSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Setting Cache
            cache.set(name, serializer.data, timeout=CACHE_TTL)
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def func(request):
    queryset = Book.objects.all()
    serializer = BookSerializer(queryset, many=True)
    return Response(serializer.data)