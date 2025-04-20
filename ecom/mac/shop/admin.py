from django.contrib import admin
from shop import models
from django.contrib.auth.models import User
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'email')  # Display these fields in the list view
    search_fields = ('order_id', 'email')  # Allow searching by order ID and email


# Register the User model in admin
# Register your models here.
admin.site.register(models.Orders)
admin.site.register(models.Product)
admin.site.register(models.Contact)
admin.site.register(models.UpdateOrders)
admin.site.register(models.categories)
