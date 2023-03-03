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
from webapps2023 import views

app_name = 'webapp'

urlpatterns = [
    path('webapps2023/login/', auth_views.LoginView.as_view(template_name='webapp/login.html'), name='login'),
    path('webapps2023/logout/', auth_views.LogoutView.as_view(next_page='/webapps2023/login/'), name='logout'),
    path('webapps2023/signup/', views.SignUpView.as_view(), name='signup'),
    path('webapps2023/profile/', views.ProfileView.as_view(), name='profile'),
    path('webapps2023/make-payment-request/', views.make_payment_request, name='make_payment_request'),
    path('webapps2023/view-payment-requests/', views.view_payment_requests, name='view_payment_requests'),
    path('webapps2023/accept-payment-request/<int:request_id>/', views.accept_payment_request, name='accept_payment_request'),
    path('webapps2023/admin/', views.admin_panel, name='admin_panel'),
    path('webapps2023/admin/edit-user/<int:user_id>/', views.edit_user, name='edit_user')
]
