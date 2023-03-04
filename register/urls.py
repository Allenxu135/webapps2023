from django.urls import path
from .views import HomePageView, SignUpView, UserProfileView, PaymentRequestView, PaymentRequestListView, \
    accept_payment_request, PaymentListView

app_name = 'register'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('payment_request/', PaymentRequestView.as_view(), name='payment_request'),
    path('payment_request_list/', PaymentRequestListView.as_view(), name='payment_request_list'),
    path('accept_payment_request/<int:request_id>/', accept_payment_request, name='accept_payment_request'),
    path('payment_list/', PaymentListView.as_view(), name='payment_list'),
]
