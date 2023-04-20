from django.urls import path

from . import views
from .views import HomePageView, SignUpView, UserProfileView, PaymentRequestView, PaymentRequestListView, \
    AcceptPaymentRequestView, PaymentListView,LoginView
from django.contrib.auth import views as auth_views


app_name = 'register'

urlpatterns = [
    path('', HomePageView.as_view(), name='webapps2023/home.html'),
    path('signup/', SignUpView.as_view(), name='webapps2023/signup.html'),
    path('UserProfile/', UserProfileView.as_view(), name='webapps2023/UserProfile.html'),
    path('payment_request/', PaymentRequestView.as_view(), name='webapps2023/payment_request.html'),
    path('payment_request_list/', PaymentRequestListView.as_view(), name='webapps2023/payment_request_list.html'),
    path('accept_payment_request/', AcceptPaymentRequestView.as_view(), name='webapps2023/accept_payment_request.html'),
    path('payment_list/', PaymentListView.as_view(), name='webapps2023/payment_list.html'),
    path('login/', LoginView.as_view(template_name='webapps2023/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='webapps2023/logout.html'),

]
