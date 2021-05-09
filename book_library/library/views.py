from rest_framework import generics, permissions
from .serializers import BookSerializer, HistorySerializer, OrderSerializer
from .models import Book, History, Order
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


class OrderCreate(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)