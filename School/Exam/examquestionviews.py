from django.shortcuts import render , get_object_or_404 , get_list_or_404 , redirect ,HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageExamQuestionsView(request,id):
    user = request.user.groups.values('name')
    questions = []
    marks = int('0')
    for i in ExamQuestions.objects.all():
        if str(i.exam.pk) == str(id):
            questions.append(i)
            marks = marks + i.marks
    context = {
        'user':user ,
        'exam':id,
        'marks':marks,
        'questions':questions,
    }
    return render(request,'Exam/ExamQuestions.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageExamAddQuestionsView(request,id):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        form = ManageExamQuestionsForm(request.POST)
        if form.is_valid:
            form.save()
            context = { 
                'user':user ,
                'return': 'Has Been Added SuccessFully'
            }
            return render(request,'Exam/ExamQuestionCreated.html',context)
        else:
            context = { 
                'user':user ,
                'return': 'Is Not Valid'
            }
            return render(request,'Exam/ExamQuestionCreated.html',context)
    else:
        form = ManageExamQuestionsForm()
        context = { 
            'exam':id,
            'user':user ,
            'form': form
        }
        return render(request ,'Exam/ExamQuestionCreate.html', context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageExamEditQuestionsView(request,id):
    user = request.user.groups.values('name')
    data = get_object_or_404(ExamQuestions, pk = id)
    if request.method == 'POST':
        form = ManageExamQuestionsForm(request.POST or None, instance=data)
        if form.is_valid:
            form.save()
            return redirect('school_exam:exam_questions',id)
    else:
        form = ManageExamQuestionsForm(instance=data)
        context = {
            'user':user ,
            'form' : form,
        }
        return render(request ,'Exam/ExamQuestionEdit.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageContentDeleteView(request,id):
    data = ExamQuestions.objects.filter(pk = id).delete()
    return redirect('school_exam:exam_questions',id)