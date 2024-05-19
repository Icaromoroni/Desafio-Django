from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Item, Order

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_staff')

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request'] if 'context' in kwargs else None
        super(UserSerializer, self).__init__(*args, **kwargs)

        if request and request.user and request.user.is_superuser:
            self.fields['is_staff'] = serializers.BooleanField()
        if self.instance is None:
            self.fields['username'].read_only = False

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])

        if 'is_staff' in validated_data:
            user.is_staff = validated_data['is_staff']

        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    itens = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all())

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_req = self.context['request'].user
        if not user_req.is_staff:
            self.fields['user'].required = False

    def create(self, validated_data):
        item_ids = validated_data.pop('itens')
        user_req = self.context['request'].user

        if user_req.is_staff and 'user' in validated_data:
            user = validated_data.pop('user')

        else:
            user = user_req

        order = Order.objects.create(user=user, **validated_data)
        order.itens.set(item_ids)
        order.att_total()
        return order


class OrderListSerializer(serializers.ModelSerializer):
    itens = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
    
