from django.urls import path
from .views import  *


urlpatterns = [
    path('', index, name='home'),
    path('signin/', signin, name='signin'),
    path('register/', register, name='register'),
    path('verifyotp/<int:user_id>/',verify_otp, name='verifyotp'),
    path('resend-otp/<int:user_id>/', resend_otp, name='resend_otp'),
    

    path('userproduct/<int:id>/', userproduct, name='userproduct'),
    path('singleproduct/<int:id>/', singleproduct, name='singleproduct'),
    path('search/',search,name='search'),


    path('login/',user_login,name='login'),
    path('logout/',logout, name='logout'),

    path('user/', user, name='user'),
    path('useraddress/',address_book, name='useraddress'),
    path('addaddress/<int:id>',add_address, name='addaddress'),
    path('updateprofile',updateprofile,name='updateuserprofile'),
    path('edit-address/<int:address_id>/',edit_address, name='edit_address'),

    path('orderbook/', orderbook, name='orderbook'),

    

]