from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import UserProfile, PaymentRequest, Payment
# Create your tests here.
class PaymentTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')

        self.user1_profile = UserProfile.objects.create(user=self.user1, selected_currency='GBP', balance=1000)
        self.user2_profile = UserProfile.objects.create(user=self.user2, selected_currency='USD', balance=2000)

        self.payment_request = PaymentRequest.objects.create(sender=self.user1_profile, recipient=self.user2_profile, amount=Decimal('100'), currency='GBP')

    def test_make_payment_request(self):
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(reverse('make_payment_request'), {'recipient_username': 'testuser2', 'amount': '50', 'currency': 'GBP'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PaymentRequest.objects.filter(sender=self.user1_profile, recipient=self.user2_profile, amount=Decimal('50'), currency='GBP', is_pending=True).exists())

    def test_accept_payment_request(self):
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.post(reverse('accept_payment_request', kwargs={'request_id': self.payment_request.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(PaymentRequest.objects.filter(id=self.payment_request.id).exists())
        self.assertTrue(Payment.objects.filter(sender=self.user2_profile, recipient=self.user1_profile, amount=Decimal('100'), currency='GBP').exists())
        self.assertEqual(Payment.objects.last().sender, self.user2_profile)
        self.assertEqual(Payment.objects.last().recipient, self.user1_profile)
        self.assertEqual(Payment.objects.last().amount, Decimal('100'))

