from import_export.admin import ImportExportModelAdmin
from MyApp.admin import blogsite
from .models import Tags , BlogTags , PostTags



blogsite.register(Tags,ImportExportModelAdmin)

class BlogTagsModel(ImportExportModelAdmin):
    list_display = ['blog','tag']
blogsite.register(BlogTags,BlogTagsModel)


class PostTagsModel(ImportExportModelAdmin):
    list_display = ['post','tag']
blogsite.register(PostTags,PostTagsModel)