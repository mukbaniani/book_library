from rest_framework import serializers
from .models import Book,History,Order,Branch,Todo

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
        fields = ['book', 'user', 'branch', 'start_date']

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields=['id','year','name','read']