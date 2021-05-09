from django.urls import path
from .views import BookList, HistoryView, PopularBook, OrderCreate,TodoCreate

urlpatterns = [
    path('book-list/', BookList.as_view(), name='book-list'),
    path('history/', HistoryView.as_view(), name='history'),
    path('popular/',PopularBook.as_view(),name='popular'),
    path('create-order/', OrderCreate.as_view(), name='create-order'),
    path('todo/',TodoCreate.as_view(), name='todo'),
]

