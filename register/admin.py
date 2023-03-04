# Register your models here.
from django.contrib import admin
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


# Custom admin class for PaymentRequest
class PaymentRequestAdmin(admin.ModelAdmin):
    # List display options for the admin site
    list_display = ('sender', 'recipient', 'amount', 'currency', 'is_pending', 'timestamp')
    # List filter options for the admin site
    list_filter = ('currency', 'is_pending')
    # Search fields for the admin site
    search_fields = ('sender__user__username', 'recipient__user__username')


# Register the models and their custom admin classes to the admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentRequest, PaymentRequestAdmin)
