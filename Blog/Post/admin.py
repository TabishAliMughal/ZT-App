from import_export.admin import ImportExportModelAdmin
from .models import Post, PostComment, PostReact, ReactTypes
from MyApp.admin import blogsite


blogsite.register(Post,ImportExportModelAdmin)
blogsite.register(ReactTypes,ImportExportModelAdmin)
blogsite.register(PostReact,ImportExportModelAdmin)
blogsite.register(PostComment,ImportExportModelAdmin)