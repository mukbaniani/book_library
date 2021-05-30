from rest_framework import generics, permissions
from .serializers import (BookSerializer, HistorySerializer, OrderSerializer,TodoSerializer, CountUserReadAuthorsSerializer,
                    BookRetrieveSerializer, BranchSerializer)
from .models import Book, Branch, History, Order, Quantity,Todo, User
from django.db.models import Count, F
from rest_framework.response import Response
from  .permissions import OrderDeletePermission



class BookList(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    search_fields = ['name']


class BookRetrieve(generics.ListAPIView):
    serializer_class = BookRetrieveSerializer
    
    def get_queryset(self, *args, **kwargs):
        book_id = self.kwargs.get('pk')
        book = Quantity.objects.filter(book=book_id).all()
        return book


class HistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer
    search_fields = ['return_book__book__name']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = History.objects.filter(user=self.request.user).all()
        return queryset


class BranchList(generics.ListAPIView):
    queryset = Branch.objects.all().prefetch_related('book')
    serializer_class = BranchSerializer


class RetrieveBranch(generics.RetrieveAPIView):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()


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
        

class OrderCreate(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user=self.request.user
        return Order.objects.filter(user=user)

class OrderDelete(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated, OrderDeletePermission]

    def delete(self, request, *args,pk, **kwargs):
        order=self.get_object()
        quantity = order.book.quantity_set.first()
        quantity.book_quantity += 1
        quantity.save()
        order.delete()
        return Response({"result": "delete"})


class TodoCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        return super().create(request,*args,**kwargs)

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user)

class TodoUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
