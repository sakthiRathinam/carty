# Generated by Django 3.0.7 on 2020-07-26 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_productpurchase_productpurchasemanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductPurchaseManager',
        ),
    ]