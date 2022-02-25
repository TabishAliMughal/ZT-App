from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.gis.db import models
from .models import Order, OrderItem
from mapwidgets.widgets import GooglePointFieldWidget
from static.mapsettings import CUSTOM_MAP_SETTINGS
from MyApp.admin import shopsite

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(ImportExportModelAdmin):
    list_display = ['id','paid','created', 'updated']
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
    }
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


shopsite.register(Order,OrderAdmin)