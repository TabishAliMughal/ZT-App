from MyApp.admin import discussionsite
from .models import Question , QuestionAudiance , Category , Answer
from import_export.admin import ImportExportModelAdmin

discussionsite.register(Question , ImportExportModelAdmin)
discussionsite.register(QuestionAudiance , ImportExportModelAdmin)
discussionsite.register(Category , ImportExportModelAdmin)
discussionsite.register(Answer , ImportExportModelAdmin)