# Generated by Django 3.0.7 on 2020-07-26 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_delete_productpurchasemanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpurchase',
            name='order_id',
            field=models.CharField(default='abc', max_length=120),
            preserve_default=False,
        ),
    ]