from django.urls import path
from .views import (BookList, HistoryView, PopularBook, OrderCreate,TodoCreate, 
CountUserReadAuthors, OrderDelete, BookRetrieve, BranchList, RetrieveBranch,TodoUpdate)


urlpatterns = [
    path('book-list/', BookList.as_view(), name='book-list'),
    path('history/', HistoryView.as_view(), name='history'),
    path('popular/', PopularBook.as_view(),name='popular'),
    path('create-order/', OrderCreate.as_view(), name='create-order'),
    path('delete-order/<int:pk>/', OrderDelete.as_view(),name='delete-order'),
    path('todo/', TodoCreate.as_view(), name='todo'),
    path('count-read-author/', CountUserReadAuthors.as_view(), name='count-read-authors'),
    path('book-list/<int:pk>/', BookRetrieve.as_view(), name='retrieve-book'),
    path('branch-list/', BranchList.as_view(), name='branch-list'),
    path('branch-list/<int:pk>/', RetrieveBranch.as_view(), name='branch-list'),
    path('updatetodo/<int:pk>/', TodoUpdate.as_view(), name='update-todo')

]