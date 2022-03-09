from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.decorators import login_required

from Relationships.Matching.models import Match
from .models import Candidates
from .forms import ManageCandidateCreateForm
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from App.Authentication.user_handeling import allowed_users


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Matrinomial_Public'])
def ManageRelationshipCandidateInfoView(request):
    data = []
    for i in Candidates.objects.all():
        if request.user.is_authenticated:
            if str(i.user) == str(request.user.pk):
                data = i
    context = {
        'data' : data ,
    }
    return render(request,"Candidate/Info.html",context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Matrinomial_Public'])
def ManageRelationshipCandidateInfoAddView(request):
    if request.method == 'POST':
        img_content = request.FILES.get('image')
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
            img_content = ContentFile(img_io.getvalue(),"img.jpg")
        form = ManageCandidateCreateForm(request.POST,{'image' : img_content})
        if request.user.is_authenticated:
            for i in Candidates.objects.all():
                if int(i.user) == int(request.user.pk):
                    form = ManageCandidateCreateForm(request.POST,{'image':img_content},instance=i)
        if form.is_valid:
            form.save()
        return redirect('relationships:info')
    else:
        dob = ''
        img_url = ''
        form = ManageCandidateCreateForm()
        if request.user.is_authenticated:
            for i in Candidates.objects.all():
                if int(i.user) == int(request.user.pk):
                    form = ManageCandidateCreateForm(instance=i)
                    dob = str(i.date_of_birth)
                    img_url = str(i.image.url)
        context = {
            'form' : form ,
            'dob' : dob ,
            'img_url' : img_url ,
        }
        return render(request,"Candidate/AddInfo.html",context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Matrinomial_Public'])
def ManageRelationshipCandidateMatchesListView(request):
    candidate = Candidates.objects.all().filter(user = request.user.pk)
    if candidate:
        candidate = get_object_or_404(Candidates,user = request.user.pk)
        gender = ''
        try:
            male = Match.objects.all().filter(male = candidate)
            female = Match.objects.all().filter(female = candidate)
            if male:
                my_matches = male
                gender = 'male'
            else:
                my_matches = female
                gender = 'female'
        except:
            my_matches = None
        context = {
            'my_matches' : my_matches ,
            'candidate' : candidate ,
            'gender' : gender ,
        }
    else:
        context = {
        }
    return render(request,"Candidate/Matches.html",context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['RAdmin'])
def ManageRelationshipCandidateListView(request):
    candidates = []
    for i in Candidates.objects.all():
        if str(i.matched) == 'False':
            candidates.append(i)
    context = {
        'candidates' : candidates ,
    }
    return render(request,"Candidate/List.html",context)
