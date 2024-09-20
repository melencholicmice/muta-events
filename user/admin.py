from django.contrib import admin
from user.models import User, UserPayment


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_email_verified', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_email_verified', 'is_staff')

class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('user__email', 'payment_id', 'payment_amount')
    search_fields = ('user__email', 'payment_id')

admin.site.register(User, UserAdmin)
admin.site.register(UserPayment, UserPaymentAdmin)
