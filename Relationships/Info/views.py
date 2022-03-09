from django.shortcuts import render
from Relationships.Candidate.models import Candidates

def ManageRelationshipHomeView(request):
    candidates = Candidates.objects.all().filter(matched=False)
    success_stories = Candidates.objects.all().filter(matched=True)
    context = {
        'candidates' : candidates ,
        'success_stories' : success_stories ,
    }
    return render(request,"Info/Home.html",context)
