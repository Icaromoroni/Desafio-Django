from django.urls import path
from .views import UserCreate, UserDetailUpdate, UserList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/users/', UserList.as_view()),
    path('auth/user/add/', UserCreate.as_view()),
    path('auth/user/<int:pk>/', UserDetailUpdate.as_view()),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]