# Generated by Django 3.0.7 on 2020-07-26 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_digital',
            field=models.BooleanField(default=False),
        ),
    ]
