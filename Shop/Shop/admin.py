from import_export.admin import ImportExportModelAdmin
from django.contrib.gis.db import models
from .models import Category , Product , Shops , Units , ProductImages , ProductVideos
from mapwidgets.widgets import GooglePointFieldWidget
from static.mapsettings import CUSTOM_MAP_SETTINGS
from MyApp.admin import shopsite

class CityAdmin(ImportExportModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
    }

class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['name', 'slug', 'price','available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


shopsite.register(Shops,CityAdmin)
shopsite.register(Category,CategoryAdmin)
shopsite.register(Product,ProductAdmin)
shopsite.register(Units,ImportExportModelAdmin)
shopsite.register(ProductImages,ImportExportModelAdmin)
shopsite.register(ProductVideos,ImportExportModelAdmin)