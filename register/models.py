from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    # This model represents a user profile with a selected currency and balance
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency_choices = (
        ('GBP', 'British Pound'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    )
    selected_currency = models.CharField(max_length=3, choices=currency_choices)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class PaymentRequest:
    pass


class Payment(models.Model):
    # This model represents a payment made from one user to another
    sender = models.ForeignKey(UserProfile, related_name='sent_payments', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name='received_payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency_choices = (
        ('GBP', 'British Pound'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    )
    currency = models.CharField(max_length=3, choices=currency_choices)
    is_pending = models.BooleanField(default=True) # True if the payment has not yet been completed
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_request = models.OneToOneField(PaymentRequest, on_delete=models.CASCADE, null=True, blank=True)


class PaymentRequest(models.Model):
    # This model represents a request for payment from one user to another
    sender = models.ForeignKey(UserProfile, related_name='sent_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name='received_requests', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency_choices = (
        ('GBP', 'British Pound'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    )
    currency = models.CharField(max_length=3, choices=currency_choices)
    is_pending = models.BooleanField(default=True) # True if the request has not yet been completed
    timestamp = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
