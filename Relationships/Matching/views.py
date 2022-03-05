from django.shortcuts import get_object_or_404, render , redirect
from Relationships.Candidate.models import Candidates
from django.contrib.auth.decorators import login_required
from Relationships.Matching.forms import ManageCandidateMatchForm
from .models import Match
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import User


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['RAdmin'])
def ManageRelationshipMatchingListView(request):
    user = request.user.groups.values('name')
    male = []
    female = []
    for i in Candidates.objects.all():
        if str(i.matched) == 'False':
            if str(i.gender) == str("Male"):
                match = Match.objects.all().filter().filter(male = i)
                i.matched = len(match)
                male.append(i)
            elif str(i.gender) == str("Female"):
                match = Match.objects.all().filter().filter(female = i)
                i.matched = len(match)
                female.append(i)
    # print("male = {} and female = {}".format(len(male),len(female)))
    context = {
        'user' : user ,
        'male' : male ,
        'female' : female ,
    }
    return render(request,"Matching/List.html",context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['RAdmin'])
def ManageRelationshipMatchingSaveView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        try:
            get_object_or_404(Match,male = request.POST.get('male'),female = request.POST.get('female'))
        except:
            form = ManageCandidateMatchForm({
                'user' : request.user.pk ,
                'male' : request.POST.get('male') ,
                'female' : request.POST.get('female') ,
                'male_side_agree' : 'False' ,
                'female_side_agree' : 'False' ,
                'active' : 'True' ,
                'processed' : 'False' ,
            })
            form.save()
        # Candidates.objects.filter(pk=request.POST.get('male')).update(matched=True)
        # Candidates.objects.filter(pk=request.POST.get('female')).update(matched=True)
    return redirect('relationships_matching:matched_list')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['RAdmin'])
def ManageRelationshipMatchedListView(request):
    user = request.user.groups.values('name')
    matching = []
    for i in Match.objects.all():
        i.user = get_object_or_404(User,pk = i.user)
        matching.append(i)
    context = {
        'matching' : matching ,
        'user' : user ,
    }
    return render(request,'Matching/Matched.html',context)
