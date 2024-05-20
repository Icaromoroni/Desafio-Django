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
    """
    Permissões de:<br/>
    1. Conta de Funcionário.<br/>
    1.1. Lista todos os usuários que não são funcionários.<br/><br/>
    2. Super Usuário.<br/>
    2.1. Lista todos os usuários do sistema.<br/>
    """

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


class UserCreate(generics.CreateAPIView):
    """
    Usuários:<br/>
    1. Anônimos.<br/>
    1.1 Qualquer usuário anônimo pode criar uma conta como cliente.<br/><br/>
    2. Funcionário.<br/>
    2.1. Pode criar contas para clientes.<br/><br/>
    3. Super Usuário.<br/>
    3.1. Pode criar contas para clientes e Funcionários.<br/>
    3.2. Para criar contas de super user deve setar o campo is_staff com true.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailUpdate(generics.RetrieveUpdateAPIView):
    """
    1. Method GET.<br/>
    1.1. Usuário(cliente) visualiza detalhes.<br/>
    1.2. Usuários(funcionários) visualiza detalhes de seus dados e de e dados de clientes.<br/><br/>
    2. Method PUT ou PATH.<br/>
    2.1. Usuário(cliente) atualiza seus dados.<br/>
    2.2. Usuários(funcionários) atualiza seus dados ou dados de clientes.<br/>
    """

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
    """Todos os Usuários podem listar os itens do sistema"""

    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    


class ItemDetail(generics.RetrieveAPIView):
    """Todos os usuários podem visualizar os detalhes de itens específicos"""

    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    


class ItemCreate(generics.CreateAPIView):
    """Somente Funcionários e super usuários podem criar itens"""

    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsStaffUser]
    

class ItemUpdate(generics.UpdateAPIView):
    """Somente Funcionários e super usuários podem atualizar itens"""

    permission_classes = [IsStaffUser]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    


class ItemDestroy(generics.DestroyAPIView):
    """Somente Funcionários e super usuários podem deletar itens"""

    permission_classes = [IsStaffUser]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    


class OrderList(generics.ListAPIView):
    """
    Listar Pedidos:<br/>
    1. Endpoint /api/orders/:<br/>
    1.1 Usuários com conta cliente pode listar todos os seus pedidos.<br/>
    1.2 Funcionários e super usuário lista todos os pedidos registrados no sistema.<br/><br/>
    2. Endpoint /api/orders/user/user_id:<br/>
    2.1. Funcionários ou super usuário pode visualizar os detalhes de qualquer pedido com o ID do usuário(cliente).
    """

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
    """
    Criar pedidos:<br/>
    1. Usuários com conta cliente pode criar pedidos somente para seu perfil.<br/>
    2. Funcionários e super usuário pode criar pedidos para clientes
    """
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

class OrderClienteDetail(generics.RetrieveAPIView):
    """
    Visualizar detalhe:<br/>
    1. Nesse endpoint somente o usuários com conta cliente pode visualizar somente detalhe de seus pedidos.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            return Order.objects.filter(user__pk=user.pk)
        except Order.DoesNotExist:
            raise Http404("Pedido não encontrado.")


class OrderEmployeeDetail(generics.RetrieveAPIView):
    """
    Listar detalhes de pedidos de clientes:<br/>
    1. Funcionários ou super usuários podem acessar pedidos específicos de clientes com o endpoint /api/user/<int:user_pk>/order/<int:order_pk>/.
    """

    permission_classes = [IsStaffUser]
    serializer_class = OrderListSerializer

    def get_object(self):
        user_pk = self.kwargs.get('user_pk')
        order_pk = self.kwargs.get('order_pk')
        try:
            return Order.objects.get(user__id=user_pk, id=order_pk)
        except Order.DoesNotExist:
            raise Http404("Pedido não encontrado.")

