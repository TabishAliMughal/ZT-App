from import_export.admin import ImportExportModelAdmin
from .models import Blog , Type
from MyApp.admin import blogsite



blogsite.register(Type,ImportExportModelAdmin)
blogsite.register(Blog,ImportExportModelAdmin)