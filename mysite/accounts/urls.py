from django.urls import path
from . import views
urlpatterns=[
path('',views.home,name="home"),
path('product/',views.products,name="product"),
path('customer/<str:pk>/',views.customer,name="customer"),
path('order_form/<str:pk>/',views.create_order,name="order_form"),
path('update_order/<str:pk>/',views.update_order,name="update_order"),
path('delete_order/<str:pk>/',views.delete_order,name="delete_order"),
path('login/',views.loginform,name='login'),
path('register/',views.registerform,name='register'),
path('logout/',views.logoutuser,name='logout')
]