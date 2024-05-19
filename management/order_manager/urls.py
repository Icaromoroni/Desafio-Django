from django.urls import path
from .views import (
    UserCreate,
    UserDetailUpdate,
    UserList,
    ItemList,
    ItemDetail,
    ItemCreate,
    ItemUpdate,
    ItemDestroy
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/users/', UserList.as_view()),
    path('auth/user/add/', UserCreate.as_view()),
    path('auth/user/<int:pk>/', UserDetailUpdate.as_view()),

    path('itens/', ItemList.as_view()),
    path('item/add/', ItemCreate.as_view()),
    path('item/<int:pk>/', ItemDetail.as_view()),
    path('item/up/<int:pk>/', ItemUpdate.as_view()),
    path('item/del/<int:pk>/', ItemDestroy.as_view()),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]