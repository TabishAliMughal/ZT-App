from django.shortcuts import render , get_object_or_404 , get_list_or_404 , redirect ,HttpResponse
from .models import *
from static.renderer import PdfMaker
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher','Individuals'])
def ManageClassExamView(request,id):
    user = request.user.groups.values('name')
    exam = get_object_or_404(ExamStatus,pk = id)
    questions = get_list_or_404(ExamQuestions , exam = id)
    answers = int('0')
    for i in ExamAnswers.objects.all():
        if str(i.exam.pk) == str(exam.pk):
            try:
                if i.indi_student.pk == (get_object_or_404(Indivisuals , user = request.user)).pk:
                    answers = answers + 1
            except:
                pass
    context = {
        'questions' : questions ,
        'exam' : exam ,
        'user': user ,
        'answers': answers ,
    }
    return render(request,'Exam/Exam.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher','Individuals'])
def ManageClassExamQuestionPrintView(request,id):
    user = request.user.groups.values('name')
    exam = get_object_or_404(ExamStatus,pk = id)
    questions = get_list_or_404(ExamQuestions , exam = id)
    context = {
        'questions' : questions ,
        'exam' : exam ,
        'user': user ,
    }
    pdf = PdfMaker('Exam/ExamQuestionsPrint.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher','Individuals'])
def ManageClassExamFilePrintView(request,id):
    file = get_object_or_404(ExamQuestions , exam = id)
    path = file.file
    return HttpResponse(path , 'application/pdf')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher'])
def ManageTeacherClassExamAnswersStudentSelectView(request,id,pk):
    exam = get_object_or_404(ExamStatus, pk = id)
    teacher = get_object_or_404(User , pk = pk)
    students = []
    classtud = []
    classes = []
    addedpics = []
    user = request.user.groups.values('name')
    tea = request.user
    for i in TeacherClass.objects.all():
        if str(i.teacher) == str(tea):
            if str(i.clas) == str(exam.class_name):
                classes.append(i)
    for c in classes:
        for i in TeacherClassStudents.objects.all():
            if str(i.clas.clas) == str(c.clas):
                classtud.append(i)
    for e in ExamAnswers.objects.all():
        for c in classtud:
            try:
                if str(e.teach_student.pk) == str(c.pk) and str(e.exam.pk) == str(exam.pk) :
                    addedpics.append(str(c.pk))
            except:
                pass
    for i in classtud:
        pics = addedpics.count(str(i.pk))
        students.append({
            'pk': i.pk ,
            'clas': i.clas ,
            'name': i.name ,
            'father_name': i.father_name ,
            'picsqty': pics ,
        })
    context = {
        'teacher': teacher ,
        'user': user ,
        'exam': exam ,
        'class' : students ,
    }
    return render(request,'Exam/Class.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher','Individuals'])
def ManageAddStudentExamPictureView(request,id,pk=None):
    if pk:
        student = get_object_or_404(TeacherClassStudents, pk = pk)
        v = 0
    else:
        student = get_object_or_404(Indivisuals , user = request.user)
        v = 1
    selectedexam = get_object_or_404(ExamStatus , pk = id)
    user = request.user.groups.values('name')
    form = ManageExamAnswersForm()
    tea = request.user
    if request.method == 'POST':
        if v == 0 :
            if request.FILES.get('picture'):
                image = Image.open(request.FILES.get('picture'))
                size = image.size
                image = image.convert('RGB')
                rsize = []
                rsize.append(int(275*1))
                rsize.append(int(275*(size[0]/size[1])))
                rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
                img_io = BytesIO()
                rimg.save(img_io, format='JPEG', quality=75)
                img_content = ContentFile(img_io.getvalue(),"img.jpg" )
            else:
                img_content = request.FILES.get('picture')
            filled_form  = ManageExamAnswersForm({
                'teach_student' : student.pk ,
                'indi_student' : '' ,
                'exam' : int(selectedexam.pk) ,
                'checked' : 'False' ,
            },{
                'picture' : img_content,
            })
            if filled_form.is_valid:
                filled_form.save()
        if v == 1:
            filled_form  = ManageExamAnswersForm({
                'teach_student' : '' ,
                'indi_student' : student.pk ,
                'exam' : int(selectedexam.pk) ,
                'checked' : 'False' ,
            },request.FILES)
            if filled_form.is_valid:
                filled_form.save()
        context = {
            'teacher': tea ,
            'student':student ,
            'exam': selectedexam ,
            'form' : form ,
            'student': student ,
            'user': user ,
        }
        return render(request,'Exam/PapersUploaded.html',context)
    else:
        context = {
            'exam': selectedexam ,
            'form': form ,
            'student': student ,
            'user': user ,
        }
        return render(request,'Exam/PapersUpload.html',context)
