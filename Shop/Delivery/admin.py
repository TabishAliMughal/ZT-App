from import_export.admin import ImportExportModelAdmin
from .models import *
from mapwidgets.widgets import GooglePointFieldWidget
from static.mapsettings import CUSTOM_MAP_SETTINGS
from MyApp.admin import shopsite


class CityAdmin(ImportExportModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
    }

shopsite.register(DeliveryPerson)
shopsite.register(DeliveryTasks,CityAdmin)
shopsite.register(DeliveryProof)

