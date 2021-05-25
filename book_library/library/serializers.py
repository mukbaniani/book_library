from rest_framework import serializers
from .models import Book, Branch, History, Order, Quantity, Todo
from django.utils.translation import gettext_lazy as _


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','name','author','Condition']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id','return_time','return_book','user','condition']


    def to_representation(self,instance):
        rep=super(HistorySerializer,self).to_representation(instance)
        rep['return_book'] = instance.return_book.name
        rep['user'] = instance.user.passport_id
        return rep


class OrderSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format="%Y-%m-%d")
    user = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Order
        fields = ['book', 'user', 'branch', 'start_date']

    def validate(self, attrs):
        address = attrs.get('branch')
        book = attrs.get('book')
        print(address, book)
        if_exists = Branch.objects.filter(
            address=address
        ).first().book.filter(
            name=book
        ).exists()
        if if_exists is False:
            error_message = f'{address} - ს ფილიალში {book} არ მოიძებნა'
            raise serializers.ValidationError(error_message)
        return attrs


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
        model = Todo
        fields = ['user','year','name','read']


class BookRetrieveSerializer(serializers.ModelSerializer):
    book_quantity = serializers.CharField(
        label = _('მარაგი'),
        read_only = True,
    )
    book = serializers.CharField(
        label=_('წიგნი'),
        read_only=True
    )
    branch = serializers.CharField(
        label=_('ფილიალი'),
        read_only=True
    )
    class Meta:
        model = Quantity
        fields = ['book_quantity', 'book', 'branch']