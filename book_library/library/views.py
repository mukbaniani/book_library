from rest_framework import generics
from library.serializers import BookSerializer,HistorySerializer,OrderSerializer
from .models import Book,History,Order
from django.db.models import Q,Count

class BookList(generics.ListAPIView):
    serializer_class = BookSerializer


    def get_queryset(self, *args, **kwargs):
        queryset = Book.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)|
                Q(author__icontains=query)
            ).distinct()
        return queryset



class HistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer


    def get_queryset(self,*args,**kwargs):
        queryset=History.objects.all()
        query=self.request.GET.get('q')
        if query:
            queryset=queryset.filter(
                Q(return_book__name__icontains=query) |
                Q(user__passport_id__icontains=query)
            ).distinct()
        return queryset

class PopularBook(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset=Order.objects.annotate(Count('book__name'))[:10]
        return queryset