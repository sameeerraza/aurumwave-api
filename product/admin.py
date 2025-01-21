from django.contrib import admin
from product.models import Product, Order, Tag

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
