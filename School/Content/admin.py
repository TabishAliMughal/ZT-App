from import_export.admin import ImportExportModelAdmin
from MyApp.admin import schoolsite
from .models import *

schoolsite.register(Content,ImportExportModelAdmin)
schoolsite.register(Module,ImportExportModelAdmin)
schoolsite.register(Videos,ImportExportModelAdmin)
schoolsite.register(Images,ImportExportModelAdmin)


