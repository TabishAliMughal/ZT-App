from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .user_handeling import unauthenticated_user
from .forms import CreateUserForm
from django.contrib import messages

def loginPage(request):
	if request.user.is_authenticated:
		logout(request)
	if request.POST.get('path'):
		path = request.POST.get('path')
	else:
		path = '/'
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(path)
		else:
			return HttpResponseRedirect(path)
	else:
		return HttpResponseRedirect(path)

def logoutUser(request):
	logout(request)
	return redirect('main')

@unauthenticated_user
def AskRegister(request):
	if request.method == "POST":
		data = request.POST.get('type')
		return redirect('register',data)
	else:
		abc = Group.objects.all()
		context = {
			'group' : abc ,
		}
		return render(request , 'Authentication/RegisterAsk.html', context)

# @unauthenticated_user
def Register(request,id):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name=id)
			user.groups.add(group)
			messages.success(request, 'Account was created for ' + username)
			return redirect('main')
	context = {
		'type':id,
        'form':form,
        }
	return render(request, 'Authentication/Register.html', context)

# @admin_only
# @login_required(login_url='main_login')
# @allowed_users(allowed_roles=['admin'])