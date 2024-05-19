from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

User = get_user_model()

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itens = models.ManyToManyField(Item, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Order {self.id} - {self.user.username}'
    
    def att_total(self):
        total = sum(item.price for item in self.itens.all())
        self.total = total
        self.save()

@receiver(m2m_changed, sender=Order.itens.through)
def att_total_order(sender, instance, **kwargs):
    if kwargs['action'] in ['post_add', 'post_remove', 'post_clear']:
        instance.att_total()
