from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    itens = models.ManyToManyField(Item)
    data_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order {self.id} - {self.usuario.username}'
