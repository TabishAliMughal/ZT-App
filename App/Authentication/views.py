from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .user_handeling import unauthenticated_user
from .forms import CreateUserForm
from django.contrib import messages
from App.User.models import UserData

def HandleUser(request):
	user = request.user.groups.values('name')
	roles = []
	for i in user:
		roles.append(i.get('name'))
	if "Shop_Creator" not in roles and "Delivery" not in roles:
		request.user.groups.add(Group.objects.get(name='Shop_Public'))
	if "Individuals" not in roles and "Admin" not in roles and "DataHandler" not in roles and "Checker" not in roles and "School" not in roles and "Parent" not in roles and "Teacher" not in roles:
		request.user.groups.add(Group.objects.get(name='School_Public'))
	if "Blog_Creator" not in roles:
		request.user.groups.add(Group.objects.get(name='Blog_Public'))
	if "RAdmin" not in roles:
		request.user.groups.add(Group.objects.get(name='Matrinomial_Public'))
	request.user.groups.add(Group.objects.get(name='Questionare_Public'))
	request.session['user'] = [i.get('name') for i in user]
	request.session['cur_user'] = get_object_or_404(UserData , user = request.user.pk).pk
	request.session.save()


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
			HandleUser(request)
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