from django.urls import path
from .views import Registration, Login, Logout

urlpatterns = [ 
    path('register/', Registration.as_view(), name='user-registration'),
    path('login/', Login.as_view(), name='login-user'),
    path('logout/', Logout.as_view(), name='logout-user')
]