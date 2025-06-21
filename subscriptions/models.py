from django.db import models
from django.contrib.auth.models import User
from sweets.models import Sweet
from django.utils import timezone
from datetime import timedelta


class PickNMixSubscription(models.Model):
    DELIVERY_CHOICES = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Every 2 Weeks'),
        ('monthly', 'Monthly'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sweet_types = models.CharField(max_length=255)
    flavor_preferences = models.CharField(max_length=255)
    explorer = models.BooleanField(default=False)
    delivery_frequency = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    next_billing_date = models.DateField(null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s PickNMix Subscription"

    def get_next_billing(self):
        if self.delivery_frequency == 'weekly':
            return self.next_billing_date + timedelta(days=7)
        elif self.delivery_frequency == 'biweekly':
            return self.next_billing_date + timedelta(days=14)
        return self.next_billing_date + timedelta(days=30)