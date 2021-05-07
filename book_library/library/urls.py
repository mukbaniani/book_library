from django.urls import path
from .views import BookList,HistoryView,PopularBook

urlpatterns = [
    path('book-list/', BookList.as_view(), name='book-list'),
    path('history/', HistoryView.as_view(), name='history'),
    path('popular/',PopularBook.as_view(),name='popular'),
]

