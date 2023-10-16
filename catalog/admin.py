from django.contrib import admin

from catalog.models import Product, ProductAccess


class CatalogAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, CatalogAdmin)
admin.site.register(ProductAccess, CatalogAdmin)
