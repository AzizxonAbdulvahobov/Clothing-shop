# from django.contrib import admin
# from . import models
# # Register your models here.

# admin.site.register(models.Category)
# admin.site.register(models.Product)

# from django.apps import apps
from django.contrib import admin
from django.utils.safestring import mark_safe
from . import models

# Register your models here

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_image')
    
    @admin.display(description='Image')
    def get_image(self, category):
        if category.img:
            return mark_safe(f'<img src="{category.img.url}" width="75px;">')
        return "No Image"

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'body', 'price', 'discount', 'quantity', 'category', 'get_image')
    list_display_links = ('id', 'name')

    @admin.display(description='Image')
    def get_image(self, product):
        if product.img:
            return mark_safe(f'<img src="{product.img.url}" width="75px;">')
        return "No Image"


