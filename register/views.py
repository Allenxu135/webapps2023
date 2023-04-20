from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from .models import UserProfile, PaymentRequest, Payment
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
class HomePageView(TemplateView):
    """
    Home page view that displays a welcome message.
    """
    template_name = 'webapps2023/home.html'



class SignUpView(CreateView):
    # Sign up view that allows new users to register.
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'webapps2023/signup.html'
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = request.POST['email']
            # check email
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email has already been used.')
                return render(request, 'webapps2023/signup.html', {'validateError': True, 'validateForm': form})
            form.save()
            user = authenticate(username=username, password=raw_password)
            user.email = email
            user.save()
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.selected_currency = request.POST['currency_choices']
            user_profile.save()
            login(request, user)
            messages.success(request, 'Resgister sucessful！Please click back to login')
        return render(request, 'webapps2023/signup.html', {'validateError': True, 'validateForm': form})

@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    """
    User profile view that displays the authenticated user's profile.
    """
    template_name = 'webapps2023/UserProfile.html'
    context = []
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user

        user = User.objects.get(username=self.request.user)
        user_profile = UserProfile.objects.get(user_id=user.pk)
 
        context['currency'] = user_profile.selected_currency
        context['balance'] = user_profile.balance
        
        # user_profile = UserProfile.objects.get(user=self.request.user)
        payment_requests = Payment.objects.filter(Q(sender=user_profile) | Q(recipient=user_profile))
        # payment_requests = PaymentRequest.objects.filter(Q(recipient=user_profile))
        # context['payment_requests'] = payment_requests
        context['transactions'] = payment_requests
        return context
    
    def post(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        other_username = request.POST['other']
        context = []
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        print(self.request.user)
        context['username'] = self.request.user
        user_profile = UserProfile.objects.get(user_id=user.pk)
        context['currency'] = user_profile.selected_currency
        context['balance'] = user_profile.balance
        
        # user_profile = UserProfile.objects.get(user=self.request.user)
        payment_requests = Payment.objects.filter(Q(sender=user_profile) | Q(recipient=user_profile))
        # payment_requests = PaymentRequest.objects.filter(Q(recipient=user_profile))
        # context['payment_requests'] = payment_requests
        context['transactions'] = payment_requests
        if not other_username:
            context['userTips'] = f'recipient_username is empty.'
            return render(request, 'webapps2023/UserProfile.html', context = context)
        
        currency = request.POST['currency']
        
        other_user = User.objects.filter(username=other_username).first()
        if not other_user:
            context['userTips'] = f' {other_username} is does not exist.'
            return render(request, 'webapps2023/UserProfile.html', context = context)
        if request.POST['amount'].isdecimal():
            amount = Decimal(request.POST['amount'])
        else:
            context['balanceTips'] = 'amount must be Decimal'
            return render(request, 'webapps2023/UserProfile.html', context=context)
        if other_user == self.request.user:
            context['userTips'] = f"You can't transfer money to yourself."
            return render(request, 'webapps2023/UserProfile.html', context=context)
        # other_user_profile = UserProfile.objects.get(user=other_user)

        if user_profile.balance < amount:
            context['balanceTips'] = 'Insufficient balance.'
            return render(request, 'webapps2023/UserProfile.html', context = context)

        # payment_request = PaymentRequest(
        #     sender=user_profile,
        #     recipient=other_user_profile,
        #     amount=amount,
        #     currency=currency,
        # )
        # payment_request.save()
        self.request.session['other_name'] = other_username
        self.request.session['amount'] = str(Decimal(amount).quantize(Decimal('0.00')))
        messages.success(request, f'The payment request of {currency} {amount} has been sent to {other_username}.')
        return redirect('/payment_request/')


@method_decorator(login_required, name='dispatch')
class PaymentRequestView(CreateView):
    """
    Payment request view that allows users to create payment requests.
    """
    model = PaymentRequest
    fields = ['recipient', 'amount', 'currency']
    template_name = 'webapps2023/payment_request.html'
    success_url = reverse_lazy('payment_request_list')

    def form_valid(self, form):
        # Set the sender profile to the authenticated user's profile
        form.instance.sender = UserProfile.objects.get(user=self.request.user)
        return super().form_valid(form)
    context = []
   
    def get_context_data(self, **kwargs):
        other_name = self.request.session.pop('other_name')
        other_amount = self.request.session.pop('amount')
        context = super().get_context_data(**kwargs)
        context['other_name'] = other_name
        context['other_amount'] = other_amount
        user = User.objects.get(username=self.request.user)
       
        user_profile = UserProfile.objects.get(user_id=user.pk)
 
        context['currency'] = user_profile.selected_currency
        context['balance'] = user_profile.balance
        return context
    
    def post(self, request):
        recipient_username = request.POST['recipient_username']
        user_profile=UserProfile.objects.get(user=self.request.user)
        currency = request.POST['currency']
        recipient_user = User.objects.filter(username=recipient_username).first()
        if not recipient_user:
            return render(request, 'webapps2023/payment_request.html', {'balanceTips': f'User {recipient_username} does not exist.'})
        if recipient_user == self.request.user:
            return render(request, 'webapps2023/payment_request.html', {'balanceTips': f"You can't request money from yourself."})
        recipient_user_profile = UserProfile.objects.get(user=recipient_user)
        print(recipient_user_profile)
        
        amount = Decimal(request.POST['amount'])
        payment_request = PaymentRequest(
            sender=user_profile,
            recipient=recipient_user_profile,
            amount=amount,
            currency=currency,
        )
        payment_request.save()

        messages.success(request, f'The payment request of {currency} {amount} has been sent to {recipient_username}.')
        return redirect('/payment_request_list/')



@method_decorator(login_required, name='dispatch')
class PaymentRequestListView(TemplateView):
    """
    Payment request list view that displays a list of payment requests for the authenticated user.
    """
    template_name = 'webapps2023/payment_request_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the authenticated user's profile and their payment requests
        user_profile = UserProfile.objects.get(user=self.request.user)
        # payment_requests = PaymentRequest.objects.filter(Q(sender=user_profile) | Q(recipient=user_profile))
        payment_requests = PaymentRequest.objects.filter(Q(recipient=user_profile))
        context['payment_requests'] = payment_requests
        # context['self_user', user_profile.user]
        return context

class AcceptPaymentRequestView(TemplateView):
      def get(self, request):
          return render(request, 'webapps2023/payment_request_list.html') 
      def post(self, request):
          if request.POST['request_type'] == '1':
            payment_request = get_object_or_404(PaymentRequest, id=request.POST['request_id'])
            recipient_profile = UserProfile.objects.get(user=self.request.user)
            recipient_profile.balance =float(recipient_profile.balance)+ moneyChange(payment_request.currency,recipient_profile.selected_currency ,payment_request.amount)
            recipient_profile.save()
            Payment.objects.create(sender=payment_request.sender, recipient=payment_request.recipient,
                                amount=payment_request.amount, currency=payment_request.currency, payment_request_id=payment_request.pk)
            sender_profile = UserProfile.objects.get(user = payment_request.sender.user)
            sender_profile.balance = float(sender_profile.balance)- moneyChange(payment_request.currency,recipient_profile.selected_currency ,payment_request.amount)
            sender_profile.save()
            # Delete the payment request object
            payment_request.delete()
            # context = super().get_context_data(**kwargs)
            # Get the authenticated user's profile and their payment requests
            # user_profile = UserProfile.objects.get(user=self.request.user)
            # payment_requests = PaymentRequest.objects.filter(Q(sender=user_profile) | Q(recipient=user_profile))
            # payment_requests = PaymentRequest.objects.filter(Q(recipient=user_profile))
            # context['payment_requests'] = payment_requests
            # messages.success(request, 'Payment request accepted successfully.')
            return redirect('/payment_request_list/') 
          else:
            payment_request = get_object_or_404(PaymentRequest, id=request.POST['request_id'])
            recipient_profile = UserProfile.objects.get(user=self.request.user)
            Payment.objects.create(sender=payment_request.sender, recipient=payment_request.recipient,
                                 amount=payment_request.amount, currency=payment_request.currency, payment_request_id=payment_request.pk)
            # context = super().get_context_data(**kwargs)
            # # Get the authenticated user's profile and their payment requests
            # user_profile = UserProfile.objects.get(user=self.request.user)
            # # payment_requests = PaymentRequest.objects.filter(Q(sender=user_profile) | Q(recipient=user_profile))
            # payment_requests = PaymentRequest.objects.filter(Q(recipient=user_profile))
            # context['payment_requests'] = payment_requests
            payment_request.delete()
            return redirect('/payment_request_list/') 
       
def moneyChange(currence, target, amount):
    if currence=='GBP' and target == 'EUR':
        return float(1.13) * float(amount)
    if currence == 'EUR' and target == 'GBP':
        return float(0.88) * float(amount)
    if currence == 'EUR' and target == 'USD':
        return float(1.09) * float(amount)
    if currence == 'GBP' and target == 'USD':
        return float(1.24) * float(amount)
    if currence == 'USD' and target == 'GBP':
        return float(0.81) * float(amount)
    if currence == 'USD' and target == 'EUR':
        return float(0.92) * float(amount)
    return float(1) * float(amount)

@method_decorator(login_required, name='dispatch')
def accept_payment_request(self, request, request_id):
        """
        Accept payment request view that allows users to accept payment requests.
        """
        payment_request = get_object_or_404(PaymentRequest, id=request_id)
        if request.method == 'POST':
            # Get the recipient's profile
            recipient_profile = UserProfile.objects.get(user=request.user)
            # Check if the recipient has enough balance
            if recipient_profile.balance >= payment_request.amount:
                # Deduct the payment amount from the recipient's balance
                recipient_profile.balance -= payment_request.amount
                recipient_profile.save()
                # Create a new payment object
                Payment.objects.create(sender=payment_request.sender, recipient=payment_request.recipient,
                                    amount=payment_request.amount, currency=payment_request.currency)
                # Delete the payment request object
                payment_request.delete()
                # messages.success(request, '')
                return render(request, 'webapps2023/payment_request_accept.html', {'tips': 'Payment request accepted successfully.'})  
            else:
                messages.error(request, 'Insufficient balance.')
                return redirect('payment_request_list')
        return render(request, 'webapps2023/payment_request_accept.html', {'payment_request': payment_request})  
@method_decorator(login_required, name='dispatch')
class PaymentListView(TemplateView):
    """
    Payment list view that displays a list of payments for the authenticated user.
    """
    template_name = 'webapps2023/payment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the authenticated user's profile and their payments
        user_profile = UserProfile.objects.get(user=self.request.user)
        payments = Payment.objects.filter(Q(sender=user_profile) | Q(recipient=user_profile))
        context['payments'] = payments
        return context
    
class LoginView(TemplateView):
    template_name = 'webapps2023/login.html'
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            user_profile = User.objects.filter(username = username, password=password)
            if user_profile is None:
                print('f')
                messages.error(request, 'Invalid form')
                return render(request, 'webapps2023/login.html')
            if user is not None:
                login(request, user)
                return redirect('/UserProfile/')
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'webapps2023/login.html')
        else:
            messages.error(request, 'Invalid form')
            return render(request, 'webapps2023/login.html')
        

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('webapps2023:UserProfile')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = AuthenticationForm()
    return render(request, 'webapps2023/login.html', {'form': form})
