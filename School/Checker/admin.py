from import_export.admin import ImportExportModelAdmin
from MyApp.admin import schoolsite
from .models import *


schoolsite.register(CheckerClass,ImportExportModelAdmin)
