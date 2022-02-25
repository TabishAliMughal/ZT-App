from django.shortcuts import render
from Relationships.Candidate.models import Candidates

def ManageRelationshipHomeView(request):
    user = request.user.groups.values('name')
    candidates = Candidates.objects.all().filter(matched=False)
    success_stories = Candidates.objects.all().filter(matched=True)
    context = {
        'user' : user ,
        'candidates' : candidates ,
        'success_stories' : success_stories ,
    }
    return render(request,"Info/Home.html",context)
