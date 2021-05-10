from django.core.serializers import serialize
from rest_framework import serializers
from .models import Book,History,Order,Branch,Todo, User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['id','name','author','quantity','branch','Condition']
        depth=1


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=History
        fields=['id','return_time','return_book','user','condition']


    def to_representation(self,instance):
        rep=super(HistorySerializer,self).to_representation(instance)
        rep['return_book']=instance.return_book.name
        rep['user']=instance.user.passport_id
        return rep


class OrderSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format="%Y-%m-%d")
    user=serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model=Order
        fields = ['id','book', 'user', 'branch', 'start_date']


class CountUserReadAuthorsSerializer(serializers.Serializer):
    count_authors = serializers.SerializerMethodField(
        'get_count_authos'
    )
    authors = serializers.SerializerMethodField(
        'get_author_name'
    )

    class Meta:
        fields = ['count_authors', 'authors']

    def get_count_authos(self, obj):
        return obj.get('count_author')

    def get_author_name(self, obj):
        return obj.get('order__book__author')


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields=['user','year','name','read']