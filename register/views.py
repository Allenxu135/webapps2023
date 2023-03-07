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
        # Create a new payment object
        Payment.objects.create(sender=payment_request.sender, recipient=payment_request.recipient,
                               amount=payment_request.amount, currency=payment_request.currency)
        # Delete the payment request object
        payment_request.delete()
        messages.success(request, 'Payment request accepted successfully.')
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


def signup(request):
    form = UserCreationForm()
    return render(request, 'webapps2023/signup.html', {'form': form})


def login_view(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Create a form instance with the POST data
        form = AuthenticationForm(data=request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Get the username and password from the cleaned data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authenticate the user
            user = authenticate(username=username, password=password)
            # Check if the user exists
            if user is not None:
                # Login the user
                login(request, user)
                # Redirect to the home page
                return redirect('home')
            else:
                # If the user does not exist, return to the home page and show a message
                messages.error(request, 'User does not exist, please sign up first.')
                return redirect('home')
    else:
        # If the request method is not POST, create an empty form
        form = AuthenticationForm()
    # Render the login template with the form
    return render(request, 'webapps2023/login.html', {'form': form})

