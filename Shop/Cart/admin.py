from import_export.admin import ImportExportModelAdmin
from .models import DeliveryCharge
from MyApp.admin import shopsite

# Register your models here.
shopsite.register(DeliveryCharge)