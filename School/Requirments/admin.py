from import_export.admin import ImportExportModelAdmin
from MyApp.admin import schoolsite
from .models import *

schoolsite.register(Classes,ImportExportModelAdmin)
schoolsite.register(Subjects,ImportExportModelAdmin)
schoolsite.register(ClassSubjects,ImportExportModelAdmin)
schoolsite.register(Session,ImportExportModelAdmin)
schoolsite.register(Visits,ImportExportModelAdmin)
