from rest_framework import generics
from library.serializers import BookSerializer,HistorySerializer
from .models import Book,History

class BookList(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()



class HistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer
    queryset = History.objects.all()

    # def get_queryset(self):
    #     user=self.request.user
    #     return History.objects.filter(user=user)

