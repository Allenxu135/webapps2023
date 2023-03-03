from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Payment, PaymentRequest


@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'balance': user_profile.balance,
        'selected_currency': user_profile.selected_currency,
        'sent_payments': user_profile.sent_payments.all(),
        'received_payments': user_profile.received_payments.all(),
        'sent_requests': user_profile.sent_requests.all(),
        'received_requests': user_profile.received_requests.all(),
    }
    return render(request, 'dashboard.html', context)


@login_required
def initiate_payment(request):
    if request.method == 'POST':
        recipient_username = request.POST['recipient_username']
        amount = float(request.POST['amount'])
        currency = request.POST['currency']
        recipient_user = get_object_or_404(UserProfile, user__username=recipient_username)
        sender_profile = UserProfile.objects.get(user=request.user)
        recipient_profile = UserProfile.objects.get(user=recipient_user.user)
        if sender_profile.balance >= amount:
            Payment.objects.create(sender=sender_profile, recipient=recipient_profile, amount=amount, currency=currency)
            sender_profile.balance -= amount
            sender_profile.save()
            recipient_profile.balance += amount
            recipient_profile.save()
            messages.success(request, f'Payment of {amount} {currency} was successfully sent to {recipient_username}.')
        else:
            messages.error(request, 'Insufficient funds.')
    return redirect('dashboard')


@login_required
def accept_payment_request(request, pk):
    payment_request = get_object_or_404(PaymentRequest, pk=pk)
    if payment_request.recipient.user != request.user:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('dashboard')
    if payment_request.is_pending:
        sender_profile = payment_request.sender
        recipient_profile = payment_request.recipient
        amount = payment_request.amount
        currency = payment_request.currency
        if recipient_profile.balance >= amount:
            Payment.objects.create(sender=sender_profile, recipient=recipient_profile, amount=amount, currency=currency)
            recipient_profile.balance -= amount
            recipient_profile.save()
            sender_profile.balance += amount
            sender_profile.save()
            payment_request.is_pending = False
            payment_request.save()
            messages.success(request, f'Payment of {amount} {currency} was successfully accepted.')
        else:
            messages.error(request, 'Insufficient funds.')
    else:
        messages.error(request, 'This payment request has already been accepted or rejected.')
    return redirect('dashboard')


@login_required
def reject_payment_request(request, pk):
    payment_request = get_object_or_404(PaymentRequest, pk=pk)
    if payment_request.recipient.user != request.user:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('dashboard')
    if payment_request.is_pending:
        payment_request.is_pending = False
        payment_request.save()
        messages.success(request, 'Payment request was successfully rejected.')
    else:
        messages.error(request, 'This payment request has already been accepted or rejected.')
    return redirect('dashboard')


class PaymentRequestForm:
    pass


@login_required
def make_payment_request(request):
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient_username']
            amount = form.cleaned_data['amount']
            currency = form.cleaned_data['currency']
            recipient_profile = get_object_or_404(UserProfile, user__username=recipient_username)
            sender_profile = UserProfile.objects.get(user=request.user)

            if sender_profile.balance < amount:
                messages.error(request, 'Insufficient funds')
                return redirect('make_payment_request')

            payment_request = PaymentRequest(sender=sender_profile, recipient=recipient_profile, amount=amount, currency=currency)
            payment_request.save()

            messages.success(request, 'Payment request sent')
            return redirect('view_payment_requests')

    else:
        form = PaymentRequestForm()

    return render(request, 'register/payment_request.html', {'form': form})

