# Generated by Django 3.0.7 on 2021-04-03 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0006_auto_20210403_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='customersmodel',
            name='customerStatus',
            field=models.CharField(default='false', max_length=10),
        ),
    ]
