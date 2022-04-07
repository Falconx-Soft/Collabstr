from multiprocessing import context
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
# from .models import join_influencer

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



def join_as_influencer(request):
	if request.method== 'POST':
		try:
			influencer_username= request.POST.get('influencer_username')
			if JoinInfluencer.objects.filter(influencer_username=influencer_username):
				messages.success(request, 'Username is taken')
				return redirect(request, 'join_as_influencer.html')
			else:

				influencer= JoinInfluencer.objects.create(influencer_username= influencer_username)
				influencer.save()
				context= {'influencer_username': influencer_username}
				return render(request,'User/create_your_page.html', context)
		except Exception as e:
			print(e)
	return render(request,'User/join_as_influencer.html')


def create_your_page(request):
	if request.method== 'POST':
		influencer_username_2= request.POST.get('influencer_username_2')
		fullname_influencer= request.POST.get('fullname')
		email_influencer= request.POST.get('email')
		password_influencer= request.POST.get('password')
		influencer=JoinInfluencer.objects.get(influencer_username= influencer_username_2)
		print('influencer', influencer)
		influencer.full_name=fullname_influencer
		influencer.email_address=email_influencer
		influencer.password=password_influencer
		influencer.save()
		# influencer= JoinInfluencer.objects.create(influencer_username= influencer_username_2)
		context= {'influencer_username_2': influencer_username_2}
		return render(request,'User/join_influencer_profile.html', context)
	return render(request,'User/create_your_page.html')



def join_influencer_profile(request):
	if request.method == 'POST':
		influencer_username_3= request.POST.get('influencer_username_3')
		location= request.POST.get('location_influencer')
		title_influencer= request.POST.get('title_influencer')
		description_influencer= request.POST.get('description_influencer')
		gender_influencer= request.POST.get('gender_influencer')
		instagram_username= request.POST.get('instagram_username')
		instagram_followers= request.POST.get('instagram_followers')
		tiktok_username= request.POST.get('tiktok_username')
		tiktok_followers= request.POST.get('tiktok_followers')
		youtube_username= request.POST.get('youtube_username')
		youtube_followers= request.POST.get('youtube_followers')
		twitter_username= request.POST.get('twitter_username')
		twitter_followers= request.POST.get('twitter_followers')
		twitch_username= request.POST.get('twitch_username')
		twitch_followers= request.POST.get('twitch_followers')
		website= request.POST.get('website')
		niches= request.POST.get('niches_val')
		profile_image= request.FILES.get('profile_img')
		cover_image= request.FILES.get('cover_image')
		img2= request.FILES.get('img2')
		img3= request.FILES.get('img3')
		img4= request.FILES.get('img4')

		influencer=JoinInfluencer.objects.get(influencer_username= influencer_username_3)
		influencer.location=location
		influencer.title_influencer=title_influencer
		influencer.description_influencer=description_influencer
		influencer.gender_influencer=gender_influencer
		influencer.instagram_username=instagram_username
		influencer.instagram_followers=instagram_followers
		influencer.tiktok_username=tiktok_username
		influencer.tiktok_followers=tiktok_followers
		influencer.youtube_url=youtube_username
		influencer.youtube_followers=youtube_followers
		influencer.twitter_username=twitter_username
		influencer.twitter_followers=twitter_followers
		influencer.twitch_username=twitch_username
		influencer.twitch_followers=twitch_followers
		influencer.website=website
		influencer.profile_image=profile_image
		influencer.cover_image=cover_image
		influencer.image3=img2
		influencer.image4=img3
		influencer.image5=img4
		if "Lifestyle" in niches:
			influencer.lifestyle= True
		if "Fashion" in niches:
			influencer.fashion= True
		if "Beauty" in niches:
			influencer.beauty= True
		
		if "Health & Fitness" in niches:
			influencer.health_fitness= True
		if "Travel" in niches:
			influencer.travel= True
		if "Food & Drink" in niches:
			influencer.food_drink= True
		if "Model" in niches:
			influencer.model= True
		if "Comedy & Entertainment" in niches:
			influencer.comedy_entertainment= True
		if "Art & Photography" in niches:
			influencer.art_photography= True
		
		if "Music & Dance" in niches:
			influencer.music_dance= True
		if "Entrepreneur & Business" in niches:
			influencer.entrepreneur_business= True
		if "Family & Children" in niches:
			influencer.family_children= True
		if "Animals & Pets" in niches:
			influencer.animals_pets= True
		if "Athlete & Sports" in niches:
			influencer.athlete_sports= True
		if "Celebrity & Public Figure" in niches:
			influencer.celebrity_public_pigure= True
		
		if "Adventure & Outdoors" in niches:
			influencer.adventure_outdoors= True
		if "Actor" in niches:
			influencer.actor= True
		if "Education" in niches:
			influencer.education= True
		if "Gaming" in niches:
			influencer.gaming= True
		if "LGBTQ2" in niches:
			influencer.lgbtq= True
		if "Technology" in niches:
			influencer.technology= True
		
		if "Healthcare" in niches:
			influencer.healthcare= True
		if "Vegan" in niches:
			influencer.vegan= True
		if "Cannabis" in niches:
			influencer.food_drcannabisink= True
		if "Skilled Trades" in niches:
			influencer.skilled_trades= True
		if "Automotive" in niches:
			influencer.automotive= True
		influencer.save()
		print('##########################')
		print('location_influencer',location)
		print('**************************')
		print('title_influencer',title_influencer)
		print('**************************')
		print('description_influencer',description_influencer)
		print('**************************')
		print('instagram_username',instagram_username)
		print('**************************')
		print('instagram_followers',instagram_followers)
		print('**************************')
		print('tiktok_username',tiktok_username)
		print('**************************')
		print('niches',niches)
		return render(request,'User/join_influencer_profile.html')
	