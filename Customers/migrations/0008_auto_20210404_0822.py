# Generated by Django 3.0.7 on 2021-04-04 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0007_customersmodel_customerstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersmodel',
            name='customerStatus',
            field=models.BooleanField(default=False),
        ),
    ]
