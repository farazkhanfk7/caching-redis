from rest_framework.views import APIView
from .models import Book
from .serializer import BookSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes

# Create your views here.
@permission_classes((permissions.AllowAny,))
class BookView(APIView):

    def get_queryset(self):
        return Book.objects.all()
    
    def get(self, request, fromat=None):
        queryset = self.get_queryset()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
