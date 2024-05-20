from django.urls import path
from . import views


urlpatterns = [
    # Usuarios
    path('auth/users/', views.UserList.as_view()),
    path('auth/user/add/', views.UserCreate.as_view()),
    path('auth/user/<int:pk>/', views.UserDetailUpdate.as_view()),
    # Itens
    path('itens/', views.ItemList.as_view()),
    path('item/add/', views.ItemCreate.as_view()),
    path('item/<int:pk>/', views.ItemDetail.as_view()),
    path('item/up/<int:pk>/', views.ItemUpdate.as_view()),
    path('item/del/<int:pk>/', views.ItemDestroy.as_view()),
    # Orders
    path('orders/', views.OrderList.as_view()),
    path('order/add/', views.OrderCreate.as_view()),
    path('order/<int:pk>/', views.OrderClienteDetail.as_view()),
    path('orders/user/<int:pk>/', views.OrderList.as_view()),
    path('user/<int:user_pk>/order/<int:order_pk>/', views.OrderEmployeeDetail.as_view()),
]