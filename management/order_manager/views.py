from .models import Item, Order
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ItemSerializer, OrderSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password



User = get_user_model()


class UserList(generics.ListAPIView):
    """Somente usuários(funcionários) e administradores podem listar todos os usuários clientes"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and user.is_superuser:
            return User.objects.all()
        elif user.is_staff and not user.is_superuser:
            return User.objects.filter(is_superuser=False, is_staff=False)
        else:
            self.permission_denied(self.request)


class UserCreate(generics.ListCreateAPIView):
    """Qualquer usuário anônimo pode criar uma conta de usuário(cliente)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailUpdate(generics.RetrieveUpdateAPIView):
    """Usuário(cliente) visualiza detalhes ou atualiza seus dados, 
    usuários(funcionários) visualiza detalhes e atualiza seus dados e de todos os clientes"""

    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff and user.is_superuser:
            return User.objects.all()
        
        elif user.is_staff and not user.is_superuser:
            pk = self.kwargs.get('pk')

            if user.pk == pk:
                return User.objects.filter(pk=user.pk)
            
            return User.objects.filter(is_staff=False)
        
        elif not user.is_staff:
            return User.objects.filter(pk=user.pk)
        
        else:
            return User.objects.none()
        
    def perform_update(self, serializer):
        user = self.request.user

        if not user.is_superuser:
            if user.pk != serializer.instance.pk:
                self.permission_denied(self.request)

        password = self.request.data.get('password', None)
        
        if password is not None:
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password

        serializer.save()


class ItemListCreate(generics.ListCreateAPIView):
    pass


class ItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    pass


class OrderListCreate(generics.ListCreateAPIView):
    pass
