# Generated by Django 5.0.6 on 2024-05-19 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0002_alter_item_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='data_pedido',
            new_name='order_date',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='usuario',
            new_name='user',
        ),
    ]
