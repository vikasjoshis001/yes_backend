# Generated by Django 3.0.7 on 2021-04-04 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0010_auto_20210404_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersmodel',
            name='customerCredit',
            field=models.CharField(blank=True, default='0', max_length=20, null=True),
        ),
    ]
