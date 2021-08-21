# Generated by Django 3.2.3 on 2021-08-20 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount_paid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='remaining',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='tip',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True),
        ),
    ]