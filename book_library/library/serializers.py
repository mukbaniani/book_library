from rest_framework import serializers
from .models import Book,History,Order,Branch


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['id','name','author','quantity','branch','Condition']
        depth=1


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=History
        fields=['id','return_time','return_book','condition']

        def get_return_book(self,obj):
            return obj.return_book.name


