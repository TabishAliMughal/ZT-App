from import_export.admin import ImportExportModelAdmin
from .models import Match
from MyApp.admin import matrinomialsite

matrinomialsite.register(Match,ImportExportModelAdmin)