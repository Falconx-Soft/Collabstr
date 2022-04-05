from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CutomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from .models import*
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
# @login_required(login_url='login')
def home(request):
	return render(request,'User/home.html')

def loginUser(request):

	if request.user.is_authenticated:
		return redirect('home')
	msg = None
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

		try:
			user = User.objects.get(email=email)
			if user:
				username = user.username
			user = authenticate(request, username=username, password=password) # check password

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				msg = 'User/Something is wrong'
		except Exception as error:
			print("error", error)
			msg = 'User not recognized.'
	context = {
		'msg':msg
	}
	return render(request,'User/login.html',context)

def register(request):
	if request.method== 'POST':
		username= request.POST.get('username')
		email= request.POST.get('email')
		password= request.POST.get('password')
		try:
			if User.objects.filter(username=username):
				messages.success(request, 'Username is taken')
				return redirect(request, 'signup.html')
			if User.objects.filter(email=email):
				messages.success(request, 'Email is already in use')
				return redirect(request, 'signup.html')
			
		
			user_obj= User(username=username, email=email)
			user_obj.set_password(password)
			user_obj.save()
		except Exception as e:
			print(e)
	return render(request,'User/register.html')





def logoutUser(request):
	logout(request)
	return redirect('login')




def join_as_brand(request):
	return render(request,'User/join_as_brand.html')