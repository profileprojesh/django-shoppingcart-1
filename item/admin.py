from django.contrib import admin
from .models import Product, OrderItem, Order, OrderInfo, Status,Updates

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(OrderInfo)
admin.site.register(Status)
admin.site.register(Updates)