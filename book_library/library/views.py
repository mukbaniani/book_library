from rest_framework import generics
from .serializers import BookSerializer, HistorySerializer
from .models import Book, History
from django.db.models import Count


class BookList(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    search_fields = ['name']


class HistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer
    queryset = History.objects.all()
    search_fields = ['return_book__name']


class PopularBook(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        books = Book.objects.annotate(popular_book=Count('order')).order_by('-popular_book')
        return books