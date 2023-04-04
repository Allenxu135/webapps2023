from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView
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
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Resgister sucessful！')
        return render(request, 'webapps2023/signup.html', {'validateError': True, 'validateForm': form})

@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    """
    User profile view that displays the authenticated user's profile.
    """
    template_name = 'webapps2023/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        return context


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
        payment_requests = PaymentRequest.objects.filter(Q(sender=user_profile) | Q(recipient=user_profile))
        context['payment_requests'] = payment_requests
        return context


@method_decorator(login_required, name='dispatch')
def accept_payment_request(request, request_id):
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
            messages.success(request, 'Payment request accepted successfully.')
            return redirect('payment_request_list')
        else:
            messages.error(request, 'Insufficient balance.')
            return redirect('payment_request_list')
    else:
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


@login_required
def my_view(request):
    # Do something here
    return render(request, 'webapps2023/my_template.html', {'data': 'some data'})


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             messages.success(request, 'Resgister sucessful！')
#             return redirect('register:webapps2023/home.html')
#     else:
#         form = UserCreationForm()
#     return render(request, 'webapps2023/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password')
                return render(request, 'webapps2023/login.html', {'form': form})
            if user is not None and user.check_password(password):
                login(request, user)
                return render(request, 'webapps2023/UserProfile.html')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = AuthenticationForm()
    return render(request, 'webapps2023/login.html', {'form': form})



