from django.db.models.expressions import F
from rest_framework import generics, permissions
from .serializers import BookSerializer, HistorySerializer, OrderSerializer,TodoSerializer, CountUserReadAuthorsSerializer
from .models import Book, History, Order,Todo, User
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
        books = Book.objects.filter(
            name=F('order__book__name')
        ).annotate(popular_book=Count('order')).order_by('-popular_book')
        return books


class CountUserReadAuthors(generics.ListAPIView):
    serializer_class = CountUserReadAuthorsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.pk
        count_user_read_author = User.objects.filter(pk=user_id).values('order__book__author').annotate(
            count_author = Count('order__book__author')
        )
        return count_user_read_author
        

class OrderCreate(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class TodoCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo
    permission_classes = [permissions.IsAuthenticated]
    search_fields=['name']

    def create(self, request, *args, **kwargs):
        return super().create(request,*args,**kwargs)

    def get_queryset(self):
        user=self.request.user

        return Todo.objects.filter(user=user)