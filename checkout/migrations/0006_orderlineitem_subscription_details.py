# Generated by Django 3.2.25 on 2025-06-21 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_order_stripe_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlineitem',
            name='subscription_details',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
