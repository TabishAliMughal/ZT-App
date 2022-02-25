
from import_export.admin import ImportExportModelAdmin
from .models import Candidates
from MyApp.admin import matrinomialsite

matrinomialsite.register(Candidates,ImportExportModelAdmin)