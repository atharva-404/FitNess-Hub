# Generated by Django 5.0.6 on 2025-02-08 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='order_id',
            field=models.CharField(default='DEFAULT_ORDER_ID', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='plan',
            field=models.CharField(choices=[('basic', 'Basic Plan'), ('standard', 'Standard Plan'), ('premium', 'Premium Plan')], max_length=20),
        ),
    ]
