# Generated by Django 3.0.7 on 2020-07-28 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20200728_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfile',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
