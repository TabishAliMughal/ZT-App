from django.shortcuts import render , get_list_or_404 , get_object_or_404 , redirect , HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from .models import *
from School.Exam.forms import *
from .forms import *
from School.Content.models import *
from School.Exam.models import *
import webbrowser as wb
from .urls import *



@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Checker'])
def ManageCheckerProfileView(request):
    user = request.user.groups.values('name')
    checker = request.user
    classes = []
    for i in CheckerClass.objects.all():
        if str(i.checker.pk) == str(checker.pk):
            classes.append(i)
    context = {
        'checker': checker ,
        'user': user ,
        'class' : classes ,
    }
    return render(request,'Checker/Profile.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Checker'])
def ManageCheckerClassView(request,pk,id):
    user = request.user.groups.values('name')
    checker = request.user
    for i in ExamStatus.objects.all():
        for k in ExamAnswers.objects.all().filter(exam = i.pk):
            print(k.exam)
    context = {
        # 'class' : classes ,
        'checker' : checker ,
        'user': user ,
        # 'students':students,
    }
    return render(request,'Checker/Class.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Checker'])
def ManageCheckerClassCreateView(request,pk):
    user = request.user.groups.values('name')
    checker = request.user
    if request.method == 'POST':
        subject = request.POST.get('subject')
        for i in CheckerClass.objects.all():
            if str(i.subject.pk) != str(subject) and str(i.checker.pk) != str(checker.pk):
                form = ManageCheckerClassCreateForm({
                    'checker': checker.pk ,
                    'subject': subject ,
                })
                form.save()
        return redirect('school_checker:checker_profile')
    else:
        form = ManageCheckerClassCreateForm()
        context = {
            'form': form ,
            'user': user ,
        }
        return render(request,'Checker/ClassCreate.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Checker'])
def ManageCheckerCheckView(request,student,checker,clas):
    user = request.user.groups.values('name')
    checker = request.user.pk
    try:
        student = get_object_or_404(Indivisuals , pk = student)
    except:
        student = get_object_or_404(TeacherClassStudents , pk = student)
    if request.method == 'POST':
        pass
    else:
        try:
            raw_answers = ExamAnswers.objects.all().filter(indi_student = student )
        except:
            raw_answers = ExamAnswers.objects.all().filter(teach_student = student )
        answers = []
        v = int('1')
        for i in raw_answers:
            answers.append({
                'code': i.code ,
                'indi_student': i.indi_student ,
                'teach_student': i.teach_student ,
                'exam': i.exam ,
                'picture': i.picture ,
                'checked': i.checked ,
                'count': v ,
            })
            v = v + 1
        total_answers = len(answers)
        context = {
            'user':user ,
            'student' : student ,
            'answers' : answers ,
            'total_answers' : total_answers ,
        }
        return render(request,'Checker/CopyCheck.html',context)
    # user = request.user.groups.values('name')
    # checker = request.user.pk
    # try:
    #     student = get_object_or_404(Indivisuals , pk = student)
    #     q = 1
    # except:
    #     student = get_object_or_404(TeacherClassStudents , pk = student)
    #     q = 2
    # checker_class = get_object_or_404(CheckerClass , pk = clas)
    # if request.method == 'POST':
    #     rawdata = request.POST
    #     v = '0'
    #     c = '0'
    #     check = request.POST.get('d')
    #     for i in rawdata:
    #         if str(i) != 'csrfmiddlewaretoken' and str(i) != "d":
    #             question = get_object_or_404(ExamQuestions , pk = i)
    #             marks = request.POST.get(i)
    #             if str(check) == 'recheck':
    #                 for v in QuestionsChecked.objects.all():
    #                     if str(checker) == str(v.checker.pk) and str(question.pk) == str(v.question.pk):
    #                         if q == 1:
    #                             if v.indi_student :
    #                                 if str(student.pk) == str(v.indi_student.pk):
    #                                     v.delete()
    #                         if q == 2:
    #                             if v.teach_student :
    #                                 if str(student.pk) == str(v.teach_student.pk):
    #                                     v.delete()
    #                 if q == 1 :
    #                     form = ManageCheckingSaveForm({
    #                         'checker' : checker ,
    #                         'question' : question.pk ,
    #                         'indi_student' : student.pk ,
    #                         'teach_student' : '' ,
    #                         'obtained' : marks ,
    #                     })
    #                     form.save()
    #                 if q == 2 :
    #                     form = ManageCheckingSaveForm({
    #                         'checker' : checker ,
    #                         'question' : question.pk ,
    #                         'indi_student' : '' ,
    #                         'teach_student' : student.pk ,
    #                         'obtained' : marks ,
    #                     })
    #                     form.save()
                        
    #             else:
    #                 if q == 1:
    #                     form = ManageCheckingSaveForm({
    #                         'checker' : checker ,
    #                         'question' : question.pk ,
    #                         'indi_student' : student.pk ,
    #                         'teach_student' : '' ,
    #                         'obtained' : marks ,
    #                     })
    #                     form.save()
    #                 if q == 2:
    #                     form = ManageCheckingSaveForm({
    #                         'checker' : checker ,
    #                         'question' : question.pk ,
    #                         'indi_student' : '' ,
    #                         'teach_student' : student.pk ,
    #                         'obtained' : marks ,
    #                     })
    #                     form.save()
    #             for ea in ExamAnswers.objects.all():
    #                 if q == 1 :
    #                     if ea.indi_student :
    #                         if str(ea.indi_student.pk) == str(student.pk):
    #                             if str(ea.exam.subject) == str(checker_class.subject.subject_name):
    #                                 if str(ea.checked) == 'False' or str(ea.checked) == 'Pending' or str(ea.checked) == 'Claimed':
    #                                     ans_form = ManageExamAnswersForm({
    #                                         'indi_student' : ea.indi_student,
    #                                         'teach_student' : ea.teach_student,
    #                                         'exam' : ea.exam ,
    #                                         'picture' : ea.picture ,
    #                                         'checker' : checker ,
    #                                         'checked' : 'True' ,
    #                                     } or None , instance = ea)
    #                                     ans_form.save()
    #                 if q == 2:
    #                     if ea.teach_student :
    #                         if str(ea.teach_student.pk) == str(student.pk):
    #                             if str(ea.exam.subject) == str(checker_class.subject.subject_name):
    #                                 if str(ea.checked) == 'False' or str(ea.checked) == 'Pending' or str(ea.checked) == 'Claimed':
    #                                     ans_form = ManageExamAnswersForm({
    #                                         'indi_student' : ea.indi_student,
    #                                         'teach_student' : ea.teach_student,
    #                                         'exam' : ea.exam ,
    #                                         'picture' : ea.picture ,
    #                                         'checker' : checker ,
    #                                         'checked' : 'True' ,
    #                                     } or None , instance = ea)
    #                                     ans_form.save()
    #     return redirect('school_checker:full_class',id,clas)
    # else:
    #     marks = '0'
    #     questions = []
    #     answers = []
    #     mar = []
    #     for d in ExamQuestions.objects.all():
    #         if q == 1 :
    #             if str(student.clas.class_name) == str(d.exam.class_name):
    #                 if str(d.exam.subject.pk) == str(checker_class.subject.subject_name.pk):
    #                     questions.append({
    #                         'pk': d.pk ,
    #                         'exam' : d.exam ,
    #                         'question' : d.question ,
    #                         'marks' : d.marks ,
    #                     })
    #                     marks = int(marks) + int(d.marks)
    #         if q == 2:
    #             if str(student.clas.clas) == str(d.exam.class_name):
    #                 if str(d.exam.subject.pk) == str(checker_class.subject.subject_name.pk):
    #                     questions.append({
    #                         'pk': d.pk ,
    #                         'exam' : d.exam ,
    #                         'question' : d.question ,
    #                         'marks' : d.marks ,
    #                     })
    #                     marks = int(marks) + int(d.marks)
    #     for i in ExamAnswers.objects.all():
    #         if q == 1 :
    #             if i.indi_student :
    #                 if str(i.indi_student.pk) == str(student.pk):
    #                     if str(i.exam.subject) == str(checker_class.subject.subject_name):
    #                         if str(i.checked) == 'False' :
    #                             a = i.picture
    #                             answers.append(a)
    #                             ans_form = ManageExamAnswersForm({
    #                                 'indi_student' : i.indi_student ,
    #                                 'teach_student' : i.teach_student ,
    #                                 'exam' : i.exam ,
    #                                 'picture' : i.picture ,
    #                                 'checker' : checker ,
    #                                 'checked' : 'Pending' ,
    #                             } or None , instance = i)
    #                             ans_form.save()
    #                         elif str(i.checked) == 'True':
    #                             marks = '0'
    #                             file = []
    #                             questions = []
    #                             for x in QuestionsChecked.objects.all():
    #                                 if x.indi_student :
    #                                     if str(x.indi_student.pk) == str(student.pk):
    #                                         if str(checker) == str(x.checker.pk):
    #                                             if str(x.question.exam.subject) == str(checker_class.subject.subject_name):
    #                                                 a = i.picture
    #                                                 answers.append(a)
    #                                                 mar.append(x.obtained)
    #                             m = '0'
    #                             for v in ExamQuestions.objects.all():
    #                                 try:
    #                                     if str(student.clas.clas) == str(i.exam.class_name):
    #                                         if str(v.exam.subject) == str(checker_class.subject.subject_name):
    #                                             questions.append({
    #                                                 'pk' : v.pk ,
    #                                                 'exam' : v.exam ,
    #                                                 'question' : v.question ,
    #                                                 'marks' : v.marks ,
    #                                                 'mar' : mar[int(m)] ,
    #                                                 'che': 'recheck' ,
    #                                             })
    #                                             marks = int(marks) + int(v.marks)
    #                                             m = int(m) + 1
    #                                 except:
    #                                     if str(student.clas.class_name) == str(i.exam.class_name):
    #                                         if str(v.exam.subject) == str(checker_class.subject.subject_name):
    #                                             questions.append({
    #                                                 'pk' : v.pk ,
    #                                                 'exam' : v.exam ,
    #                                                 'question' : v.question ,
    #                                                 'marks' : v.marks ,
    #                                                 'mar' : mar[int(m)] ,
    #                                                 'che': 'recheck' ,
    #                                             })
    #                                             marks = int(marks) + int(v.marks)
    #                                             m = int(m) + 1
    #                         elif str(i.checked) == 'Pending' :
    #                             if str(i.checker.pk) == str(checker):
    #                                 a = i.picture
    #                                 answers.append(a)
    #                             else:
    #                                 answers = 'Copies Checking Already Pending'
    #                         elif str(i.checked) == 'Claimed' :
    #                             marks = '0'
    #                             file = []
    #                             questions = []
    #                             for x in QuestionsChecked.objects.all():
    #                                 if str(x.indi_student.pk) == str(student.pk):
    #                                     if str(checker) == str(x.checker.pk):
    #                                         if str(x.question.exam.subject) == str(checker_class.subject.subject_name):
    #                                             a = i.picture
    #                                             answers.append(a)
    #                                             mar.append(x.obtained)
    #                             m = '0'
    #                             for v in ExamQuestions.objects.all():
    #                                 if str(student.clas.clas) == str(i.exam.class_name):
    #                                     if str(v.exam.subject) == str(checker_class.subject.subject_name):
    #                                         questions.append({
    #                                             'pk' : v.pk ,
    #                                             'exam' : v.exam ,
    #                                             'question' : v.question ,
    #                                             'marks' : v.marks ,
    #                                             'mar' : mar[int(m)] ,
    #                                             'che': 'recheck' ,
    #                                         })
    #                                         marks = int(marks) + int(v.marks)
    #                                         v = str(v.file)
    #                                         file.append(v[7:])
    #                                         m = int(m) + 1
    #         if q == 2 :
    #             if i.teach_student:
    #                 if str(i.teach_student.pk) == str(student.pk):
    #                     if str(i.exam.subject) == str(checker_class.subject.subject_name):
    #                         if str(i.checked) == 'False' :
    #                             a = i.picture
    #                             answers.append(a)
    #                             ans_form = ManageExamAnswersForm({
    #                                 'teach_student' : i.teach_student ,
    #                                 'exam' : i.exam ,
    #                                 'picture' : i.picture ,
    #                                 'checker' : checker ,
    #                                 'checked' : 'Pending' ,
    #                             } or None , instance = i)
    #                             ans_form.save()
    #                             print(i.teach_student)
    #                         elif str(i.checked) == 'True':
    #                             marks = '0'
    #                             file = []
    #                             questions = []
    #                             for x in QuestionsChecked.objects.all():
    #                                 if x.indi_student:                                        
    #                                     if str(x.indi_student.pk) == str(student.pk):
    #                                         if str(checker) == str(x.checker.pk):
    #                                             if str(x.question.exam.subject) == str(checker_class.subject.subject_name):
    #                                                 a = i.picture
    #                                                 answers.append(a)
    #                                                 mar.append(x.obtained)
    #                                 if x.teach_student:                                                    
    #                                     if str(x.teach_student.pk) == str(student.pk):
    #                                         if str(checker) == str(x.checker.pk):
    #                                             if str(x.question.exam.subject) == str(checker_class.subject.subject_name):
    #                                                 a = i.picture
    #                                                 answers.append(a)
    #                                                 mar.append(x.obtained)
    #                             m = '0'
    #                             for v in ExamQuestions.objects.all():
    #                                 if str(student.clas.clas) == str(i.exam.class_name):
    #                                     if str(v.exam.subject) == str(checker_class.subject.subject_name):
    #                                         questions.append({
    #                                             'pk' : v.pk ,
    #                                             'exam' : v.exam ,
    #                                             'question' : v.question ,
    #                                             'marks' : v.marks ,
    #                                             'mar' : mar[int(m)] ,
    #                                             'che': 'recheck' ,
    #                                         })
    #                                         marks = int(marks) + int(v.marks)
    #                                         m = int(m) + 1
    #                         elif str(i.checked) == 'Pending' :
    #                             if str(i.checker.pk) == str(checker):
    #                                 a = i.picture
    #                                 answers.append(a)
    #                             else:
    #                                 answers = 'Copies Checking Already Pending'
    #                         elif str(i.checked) == 'Claimed' :
    #                             marks = '0'
    #                             file = []
    #                             questions = []
    #                             for x in QuestionsChecked.objects.all():
    #                                 if str(x.student.pk) == str(student.pk):
    #                                     if str(checker) == str(x.checker.pk):
    #                                         if str(x.question.exam.subject) == str(checker_class.subject.subject_name):
    #                                             a = i.picture
    #                                             answers.append(a)
    #                                             mar.append(x.obtained)
    #                             m = '0'
    #                             for v in ExamQuestions.objects.all():
    #                                 if str(student.clas.clas) == str(i.exam.class_name):
    #                                     if str(v.exam.subject) == str(checker_class.subject.subject_name):
    #                                         questions.append({
    #                                             'pk' : v.pk ,
    #                                             'exam' : v.exam ,
    #                                             'question' : v.question ,
    #                                             'marks' : v.marks ,
    #                                             'mar' : mar[int(m)] ,
    #                                             'che': 'recheck' ,
    #                                         })
    #                                         marks = int(marks) + int(v.marks)
    #                                         v = str(v.file)
    #                                         file.append(v[7:])
    #                                         m = int(m) + 1
    #     if answers == []:
    #         answers = 'No Answers'
    #     context = {
    #         'mar' : mar ,
    #         'student' : student,
    #         'num_ans': len(answers),
    #         'answers' :answers,
    #         'marks' : marks ,
    #         'questions' : questions ,
    #         'user': user ,
    #     }
        # return render(request,'Checker/CopyCheck.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher'])
def ManageCheckerStudentCopyCheckClaimView(request,exam,student):
    user = request.user.groups.values('name')
    exam = get_object_or_404(ExamStatus , pk = exam)
    student = get_object_or_404(TeacherClassStudents , pk = student)
    for i in ExamAnswers.objects.all():
        if str(i.student.pk) == str(student.pk):
            if str(i.exam.pk) == str(exam.pk):
                ans_form = ManageExamAnswersForm({
                            'student' : i.student ,
                            'exam' : i.exam ,
                            'picture' : i.picture ,
                            'checker' : i.checker ,
                            'checked' : 'Claimed' ,
                        } or None , instance = i)
                ans_form.save()
    return redirect('school_student:student_profile',student.pk)
