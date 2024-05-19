from django.http import Http404
from .models import Item, Order
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ItemSerializer, OrderCreateSerializer, OrderListSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from .permission import IsStaffUser


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


class ItemList(generics.ListAPIView):
    """Usuário autenticado lista todos os itens"""

    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    


class ItemDetail(generics.RetrieveAPIView):
    """Usuário autenticado detalhes itens especificos"""

    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    


class ItemCreate(generics.CreateAPIView):
    """Usuários funcionarios autenticados cria itens especificos"""

    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsStaffUser]
    

class ItemUpdate(generics.UpdateAPIView):
    """Usuários funcionarios autenticados atualiza itens especificos"""

    permission_classes = [IsStaffUser]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    


class ItemDestroy(generics.DestroyAPIView):
    """Usuários funcionarios autenticados deleta itens especificos"""

    permission_classes = [IsStaffUser]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    


class OrderList(generics.ListAPIView):
    """Usuários autenticados lista seus pesidos especificos, 
    caso o usuário seja funcionario pode listar os orders do cliente fornecendo o id no endpoint"""

    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            pk = self.kwargs.get('pk')

            if pk:
                return Order.objects.filter(user__pk=pk)
            
            return Order.objects.all()
        
        return Order.objects.filter(user__pk=user.pk)

class OrderCreate(generics.CreateAPIView):
    """Usuários autenticados cria pedidos"""
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

class OrderClienteDetail(generics.RetrieveAPIView):
    """Usuários autenticados visualiza detalhe pedidos especificos"""

    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            return Order.objects.filter(user__pk=user.pk)
        except Order.DoesNotExist:
            raise Http404("Pedido não encontrado.")


class OrderEmployeeDetail(generics.RetrieveAPIView):
    """Usuários funcionarios autenticados visualiza detalhe de
    pedidos especificos de usuários especificos"""

    permission_classes = [IsStaffUser]
    serializer_class = OrderListSerializer

    def get_object(self):
        user_pk = self.kwargs.get('user_pk')
        order_pk = self.kwargs.get('order_pk')
        try:
            return Order.objects.get(user__id=user_pk, id=order_pk)
        except Order.DoesNotExist:
            raise Http404("Pedido não encontrado.")

