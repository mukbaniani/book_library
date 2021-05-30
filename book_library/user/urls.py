from django.urls import path
from .views import Registration, Login, Logout, PasswordResetRequest, PasswordUpdate,DeleteAccount

urlpatterns = [ 
    path('register/', Registration.as_view(), name='user-registration'),
    path('login/', Login.as_view(), name='login-user'),
    path('logout/', Logout.as_view(), name='logout-user'),
    path('password/reset/request/', PasswordResetRequest.as_view(), name='password-reset'),
    path('<str:uidb64>/', PasswordUpdate.as_view(), name='password-update'),
    path('deleteuser/',DeleteAccount.as_view(), name="delete-user")
]