# Generated by Django 3.0.7 on 2021-03-24 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessModel',
            fields=[
                ('businessId', models.AutoField(primary_key=True, serialize=False)),
                ('businessName', models.CharField(max_length=200)),
            ],
        ),
    ]
