from django.shortcuts import get_object_or_404, redirect, render
from App.User.models import UserData
from Discussion.Questionare.forms import AnswerQuestionForm, AskQuestionForm
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

from Discussion.Questionare.models import Answer, Question


def ManageQuestionsListView(request,user=None):
    if user:
        user = get_object_or_404(UserData , user = request.user)
        ques =  Question.objects.all().filter(user = user.pk)
    else:
        user = None
        ques = Question.objects.all()
    questions = []
    for i in ques :
        answers = []
        for k in Answer.objects.all().filter(question = i):
            k.user = get_object_or_404(UserData , pk = k.user)
            answers.append(k)
        
        i.user = get_object_or_404(UserData , pk = i.user)
        questions.append({'question':i , 'answers':answers})
    answer_form = AnswerQuestionForm()
    context = {
        'questions' : questions ,
        'answer_form' : answer_form ,
        'user' : user ,
    }
    return render(request,'Questionare/List.html',context)

def ManageUserQuestionAskView(request):
    if request.method == 'POST':
        if request.FILES.get('image'):
            image = Image.open(request.FILES.get('image'))
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
            img_content = request.POST.get('image')
        form = AskQuestionForm(request.POST,{'image':img_content , 'video' : request.FILES.get('video')})
        form.save()
        return redirect('discussion_questionare:my_question',get_object_or_404(UserData,user = request.user).pk)
    else:
        form = AskQuestionForm()
        context = {
            'form' : form ,
        }
        return render(request,'Questionare/AskQuestion.html',context)

def ManageQuestionAnswerView(request):
    if request.method == 'POST':
        print(request.POST)
        if request.FILES.get('image'):
            image = Image.open(request.FILES.get('image'))
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
            img_content = request.POST.get('image')
        form = AnswerQuestionForm(request.POST,{'image':img_content , 'video' : request.FILES.get('video')})
        form.save()
        return redirect('discussion_questionare:questions')