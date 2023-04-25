from django.contrib import admin
from homeapp.models import Category,Product,ProductImage,UserProfile,Address
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(UserProfile)
admin.site.register(Address)
