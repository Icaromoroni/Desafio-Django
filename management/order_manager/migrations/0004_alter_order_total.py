# Generated by Django 5.0.6 on 2024-05-19 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0003_rename_data_pedido_order_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
