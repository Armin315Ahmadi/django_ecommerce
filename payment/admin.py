from django.contrib import admin
from .models import ShippingAddress , Order , OrderItem
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# create an orderitem inline
class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0

# extend our order model
class OrderAdmin(admin.ModelAdmin):
    model= Order
    readnoly_field = ["date_ordered"]
    fields = ["user" , "full_name" , "email" , "shipping_address" , "amount_paid" , "date_ordered", "shipped" ,"date_shipped"]
    inlines = [OrderItemInLine]

# unregister order model
admin.site.unregister(Order)
# re - reegister our order model
admin.site.register(Order ,OrderAdmin)




