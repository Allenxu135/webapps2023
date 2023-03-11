from django.urls import path
from .views import HomePageView, SignUpView, UserProfileView, PaymentRequestView, PaymentRequestListView, \
    accept_payment_request, PaymentListView
from django.contrib.auth import views as auth_views

app_name = 'register'

urlpatterns = [
    path('', HomePageView.as_view(), name='webapps2023/home.html'),
    path('sign up/', SignUpView.as_view(),name ='webapps2023/signup.html'),
    path('profile/', UserProfileView.as_view(), name='webapps2023/profile.html'),
    path('payment_request/', PaymentRequestView.as_view(), name='webapps2023/payment_request'),
    path('payment_request_list/', PaymentRequestListView.as_view(), name='webapps2023/payment_request_list.html'),
    path('accept_payment_request/<int:request_id>/', accept_payment_request, name='webapps2023/accept_payment_request.html'),
    path('payment_list/', PaymentListView.as_view(), name='webapps2023/payment_list.html'),
    path('login/', auth_views.LoginView.as_view(template_name='webapps2023/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='webapps2023/logout.html'),
]
