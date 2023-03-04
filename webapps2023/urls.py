"""webapps2023 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomePageView, SignUpView, UserProfileView, PaymentRequestView, PaymentRequestListView, \
    accept_payment_request, PaymentListView, initiate_payment, accept_payment, reject_payment, make_payment_request

urlpatterns = [
    path('webapps2023/', HomePageView.as_view(), name='home'),
    path('webapps2023/signup/', SignUpView.as_view(), name='signup'),
    path('webapps2023/login/', auth_views.LoginView.as_view(template_name='webapps2023/login.html'), name='login'),
    path('webapps2023/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('webapps2023/profile/', UserProfileView.as_view(), name='profile'),
    path('webapps2023/payment-request/', PaymentRequestView.as_view(), name='payment_request'),
    path('webapps2023/payment-request-list/', PaymentRequestListView.as_view(), name='payment_request_list'),
    path('webapps2023/accept-payment-request/<int:request_id>/', accept_payment_request, name='accept_payment_request'),
    path('webapps2023/payment-list/', PaymentListView.as_view(), name='payment_list'),
    path('webapps2023/initiate-payment/', initiate_payment, name='initiate_payment'),
    path('webapps2023/accept-payment/<int:pk>/', accept_payment, name='accept_payment'),
    path('webapps2023/reject-payment/<int:pk>/', reject_payment, name='reject_payment'),
    path('webapps2023/make-payment-request/', make_payment_request, name='make_payment_request'),
]

