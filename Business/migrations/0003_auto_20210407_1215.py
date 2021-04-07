# Generated by Django 3.0.7 on 2021-04-07 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Business', '0002_auto_20210403_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessmodel',
            name='businessCredit',
            field=models.CharField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='businessmodel',
            name='businessDebit',
            field=models.CharField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='businessmodel',
            name='businessPending',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
