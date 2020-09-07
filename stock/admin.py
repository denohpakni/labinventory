from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Product, Category, HistConf

# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(HistConf)

# For importing data
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass

