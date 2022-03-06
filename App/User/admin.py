from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.gis.db import models
from .models import Creator , UserData
from mapwidgets.widgets import GooglePointFieldWidget
from static.mapsettings import CUSTOM_MAP_SETTINGS

# class CityAdmin(ImportExportModelAdmin):
#     formfield_overrides = {
#         models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
#     }

# admin.site.register(Creator,CityAdmin)


class CityAdmin(ImportExportModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
    }

admin.site.register(UserData,CityAdmin)
