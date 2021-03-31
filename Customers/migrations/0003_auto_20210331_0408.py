# Generated by Django 3.0.7 on 2021-03-31 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0002_transactionhistorymodel_transactioncustomer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customersmodel',
            name='customerAadharNumber',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='customersmodel',
            name='customerAddress',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='customersmodel',
            name='customerPanNumber',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transactionhistorymodel',
            name='transactionAadharNumber',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='transactionhistorymodel',
            name='transactionAddress',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='transactionhistorymodel',
            name='transactionPanNumber',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customersmodel',
            name='customerContact',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customersmodel',
            name='customerCredit',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='customersmodel',
            name='customerDebit',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='customersmodel',
            name='customerPending',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='transactionContact',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
