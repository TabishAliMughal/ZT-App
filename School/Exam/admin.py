from import_export.admin import ImportExportModelAdmin
from MyApp.admin import schoolsite
from .models import *

# Register your models here.

schoolsite.register(ExamStatus,ImportExportModelAdmin)
schoolsite.register(ExamQuestions,ImportExportModelAdmin)
schoolsite.register(ExamAnswers,ImportExportModelAdmin)
schoolsite.register(QuestionsChecked,ImportExportModelAdmin)
schoolsite.register(Guide,ImportExportModelAdmin)