from django.contrib import admin
from .models import Order, OrderProduct, Payment, PaymentGatewaySettings

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Payment)
admin.site.register(PaymentGatewaySettings)  # Registering PaymentGatewaySettings model