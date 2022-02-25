from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Bunch , BunchPost
from MyApp.admin import blogsite

# admin.site.register(Bunch)

class BunchPostInline(admin.TabularInline):
    model = BunchPost
    raw_id_fields = ['post']

class BunchAdmin(ImportExportModelAdmin):
    inlines = [BunchPostInline]

blogsite.register(Bunch,BunchAdmin)
blogsite.register(BunchPost,ImportExportModelAdmin)