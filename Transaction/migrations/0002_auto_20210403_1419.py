# Generated by Django 3.0.7 on 2021-04-03 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionhistorymodel',
            old_name='creationTime',
            new_name='transactionTime',
        ),
    ]