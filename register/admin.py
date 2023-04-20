from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import UserProfile, Payment, PaymentRequest


# Custom admin class for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    # List display options for the admin site
    list_display = ('user', 'selected_currency', 'balance')
    # Search fields for the admin site
    search_fields = ('user__username', 'user__email')


# Custom admin class for Payment
class PaymentAdmin(admin.ModelAdmin):
    # List display options for the admin site
    list_display = ('sender', 'recipient', 'amount', 'currency', 'is_pending', 'timestamp')
    # List filter options for the admin site
    list_filter = ('currency', 'is_pending')
    # Search fields for the admin site
    search_fields = ('sender__user__username', 'recipient__user__username')

    def get_changeform_link(self, obj):
        changeform_url = reverse('admin:register_payment_change', args=[obj.pk])
        return format_html('<a href="{}">View</a>', changeform_url)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


# Custom admin class for PaymentRequest
class PaymentRequestAdmin(admin.ModelAdmin):
    # List display options for the admin site
    list_display = ('sender', 'recipient', 'amount', 'currency', 'is_pending', 'timestamp')
    # List filter options for the admin site
    list_filter = ('currency', 'is_pending')
    # Search fields for the admin site
    search_fields = ('sender__user__username', 'recipient__user__username')

    def get_changeform_link(self, obj):
        changeform_url = reverse('admin:register_paymentrequest_change', args=[obj.pk])
        return format_html('<a href="{}">View</a>', changeform_url)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


# Register the models and their custom admin classes to the admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentRequest, PaymentRequestAdmin)
