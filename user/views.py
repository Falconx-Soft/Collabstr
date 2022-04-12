from multiprocessing import context
from urllib.parse import uses_netloc
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
from sms import send_sms

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
				messages.success(request, 'Something is wrong')
		except Exception as error:
			print("error", error)
			messages.success(request, 'Username Not recognized')
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
			if User.objects.filter(username=influencer_username):
				messages.success(request, 'Username Not Available')
				return redirect(request, 'join_as_influencer.html')
			else:

				influencer= User.objects.create(username= influencer_username)
				influencer.save()
				influencer_obj2= JoinInfluencer.objects.create(influencer_username= influencer_username)
				influencer_obj2.save()
				request.session['username_session'] = influencer_username
				username_session = request.session.get('username_session')
				print('Fav username_session::::::@@@@',username_session)
				context= {'influencer_username': influencer_username}
				return render(request,'User/create_your_page.html', context)
		except Exception as e:
			print(e)
	return render(request,'User/join_as_influencer.html')


def create_your_page(request):
	if request.method== 'POST':
		try:
			username_session = request.session.get('username_session')
			print('Fav username_session create page::::::@@@@',username_session)
			influencer_username_2= request.POST.get('influencer_username_2')
			fullname_influencer= request.POST.get('fullname')
			email_influencer= request.POST.get('email')
			password_influencer= request.POST.get('password')
			if User.objects.filter(email=email_influencer):
					messages.success(request, 'Email Already in use')
					return redirect('create_your_page' )
			else:
				influencer=User.objects.get(username= username_session)
				influencer_obj= JoinInfluencer.objects.get(influencer_username= username_session)
				print('influencer', influencer)
				# influencer_obj=influencer(firstname=fullname_influencer,email=email_influencer)
				influencer.first_name=fullname_influencer
				influencer.email=email_influencer
				influencer.set_password(password_influencer)
				# influencer_obj_.set_password(password_influencer)
				influencer.save()
				
				
				influencer_obj.full_name=fullname_influencer
				influencer_obj.email_address=email_influencer
				influencer_obj.password=password_influencer
				influencer_obj.save()
			context= {'influencer_username_2': influencer_username_2}
			return render(request,'User/join_influencer_profile.html', context)
		except Exception as e:
			print(e)
	return render(request,'User/create_your_page.html')



def join_influencer_profile(request):
	if request.method == 'POST':
		username_session = request.session.get('username_session')
		print('Fav username_session create page::::::@@@@',username_session)
		influencer_username_3= request.POST.get('influencer_username_3')
		influencer=JoinInfluencer.objects.get(influencer_username= username_session)
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
		cover_image= request.FILES.get('img-files')
		img2= request.FILES.get('img2')
		img3= request.FILES.get('img3')
		img4= request.FILES.get('img4')
		package_platform_0= request.POST.get('package_platform_0')
		package_platform_1= request.POST.get('package_platform_1')
		package_platform_2= request.POST.get('package_platform_2')
		package_platform_3= request.POST.get('package_platform_3')
		package_platform_4= request.POST.get('package_platform_4')
		package_platform_5= request.POST.get('package_platform_5')
		package_platform_6= request.POST.get('package_platform_6')
		package_platform_7= request.POST.get('package_platform_7')
		package_platform_8= request.POST.get('package_platform_8')
		package_platform_9= request.POST.get('package_platform_9')
		package_platform_10= request.POST.get('package_platform_10')
		package_platform_11= request.POST.get('package_platform_11')
		package_platform_12= request.POST.get('package_platform_12')
		package_platform_13= request.POST.get('package_platform_13')
		package_platform_14= request.POST.get('package_platform_14')
		package_platform_15= request.POST.get('package_platform_15')
		package_platform_16= request.POST.get('package_platform_16')
		package_platform_17= request.POST.get('package_platform_17')
		package_platform_18= request.POST.get('package_platform_18')
		package_platform_19= request.POST.get('package_platform_19')


		
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
			influencer.cannabis= True
		if "Skilled Trades" in niches:
			influencer.skilled_trades= True
		if "Automotive" in niches:
			influencer.automotive= True
		
		influencer.save()
		# ____________________________________________________________________________
		# Form no 8: all the packages
		if package_platform_0 is not None:
			package_content_type_0= request.POST.get('package_content_type_0')
			package_title_0= request.POST.get('package_title_0')
			package_description_0= request.POST.get('package_description_0')
			package_price_0= request.POST.get('package_price_0')
			if package_platform_0 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
				influencer_package.save()
			if package_platform_0 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
				influencer_package.save()
				
			if package_platform_0 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
				influencer_package.save()
				
			if package_platform_0 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
				influencer_package.save()
				
			if package_platform_0 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
				influencer_package.save()
				
			if package_platform_0 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
				influencer_package.save()
				
			
			print('##########################')
			print('package_content_type_0',package_content_type_0)
			print('**************************')
			print('package_title_0',package_title_0)
			print('**************************')
			print('package_description_0',package_description_0)
			print('**************************')
			print('package_price_0',package_price_0)
			print('package_platform_0',package_platform_0)
		if package_platform_1 is not None:
			package_content_type_1= request.POST.get('package_content_type_1')
			package_title_1= request.POST.get('package_title_1')
			package_description_1= request.POST.get('package_description_1')
			package_price_1= request.POST.get('package_price_1')
			if package_platform_1 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
				influencer_package.save()
			if package_platform_1 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
				influencer_package.save()
				
			if package_platform_1 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
				influencer_package.save()
				
			if package_platform_1 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
				influencer_package.save()
				
			if package_platform_1 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
				influencer_package.save()
				
			if package_platform_1 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
				influencer_package.save()
						
		if package_platform_2 is not None:
			package_content_type_2= request.POST.get('package_content_type_2')
			package_title_2= request.POST.get('package_title_2')
			package_description_2= request.POST.get('package_description_2')
			package_price_2= request.POST.get('package_price_2')
			if package_platform_2 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
				influencer_package.save()
			if package_platform_2 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
				influencer_package.save()
				
			if package_platform_2 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
				influencer_package.save()
				
			if package_platform_2 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
				influencer_package.save()
				
			if package_platform_2 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
				influencer_package.save()
				
			if package_platform_2 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
				influencer_package.save()
		if package_platform_3 is not None:
			package_content_type_3= request.POST.get('package_content_type_3')
			package_title_3= request.POST.get('package_title_3')
			package_description_3= request.POST.get('package_description_3')
			package_price_3= request.POST.get('package_price_3')
			if package_platform_3 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
				influencer_package.save()
			if package_platform_3 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
				influencer_package.save()
				
			if package_platform_3 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
				influencer_package.save()
				
			if package_platform_3 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
				influencer_package.save()
				
			if package_platform_3 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
				influencer_package.save()
				
			if package_platform_3 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
				influencer_package.save()	
		if package_platform_4 is not None:
			package_content_type_4= request.POST.get('package_content_type_4')
			package_title_4= request.POST.get('package_title_4')
			package_description_4= request.POST.get('package_description_4')
			package_price_4= request.POST.get('package_price_4')
			if package_platform_4 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
				influencer_package.save()
			if package_platform_4 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
				influencer_package.save()
				
			if package_platform_4 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
				influencer_package.save()
				
			if package_platform_4 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
				influencer_package.save()
				
			if package_platform_4 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
				influencer_package.save()
				
			if package_platform_4 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
				influencer_package.save()
		if package_platform_5 is not None:
			package_content_type_5= request.POST.get('package_content_type_5')
			package_title_5= request.POST.get('package_title_5')
			package_description_5= request.POST.get('package_description_5')
			package_price_5= request.POST.get('package_price_5')
			if package_platform_5 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
				influencer_package.save()
			if package_platform_5 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
				influencer_package.save()
				
			if package_platform_5 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
				influencer_package.save()
				
			if package_platform_5 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
				influencer_package.save()
				
			if package_platform_5 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
				influencer_package.save()
				
			if package_platform_5 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
				influencer_package.save()
		if package_platform_6 is not None:
			package_content_type_6= request.POST.get('package_content_type_6')
			package_title_6= request.POST.get('package_title_6')
			package_description_6= request.POST.get('package_description_6')
			package_price_6= request.POST.get('package_price_6')
			if package_platform_6 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
				influencer_package.save()
			if package_platform_6 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
				influencer_package.save()
				
			if package_platform_6 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
				influencer_package.save()
				
			if package_platform_6 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
				influencer_package.save()
				
			if package_platform_6 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
				influencer_package.save()
				
			if package_platform_6 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
				influencer_package.save()	
		if package_platform_7 is not None:
			package_content_type_7= request.POST.get('package_content_type_7')
			package_title_7= request.POST.get('package_title_7')
			package_description_7= request.POST.get('package_description_7')
			package_price_7= request.POST.get('package_price_7')
			if package_platform_7 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
				influencer_package.save()
			if package_platform_7 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
				influencer_package.save()
				
			if package_platform_7 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
				influencer_package.save()
				
			if package_platform_7 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
				influencer_package.save()
				
			if package_platform_7 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
				influencer_package.save()
				
			if package_platform_7 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
				influencer_package.save()
		if package_platform_8 is not None:
			package_content_type_8= request.POST.get('package_content_type_8')
			package_title_8= request.POST.get('package_title_8')
			package_description_8= request.POST.get('package_description_8')
			package_price_8= request.POST.get('package_price_8')
			if package_platform_8 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
				influencer_package.save()
			if package_platform_8 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
				influencer_package.save()
				
			if package_platform_8 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
				influencer_package.save()
				
			if package_platform_8 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
				influencer_package.save()
				
			if package_platform_8 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
				influencer_package.save()
				
			if package_platform_8 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
				influencer_package.save()
		if package_platform_9 is not None:
			package_content_type_9= request.POST.get('package_content_type_9')
			package_title_9= request.POST.get('package_title_9')
			package_description_9= request.POST.get('package_description_9')
			package_price_9= request.POST.get('package_price_9')
			if package_platform_9 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
				influencer_package.save()
			if package_platform_9 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
				influencer_package.save()
				
			if package_platform_9 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
				influencer_package.save()
				
			if package_platform_9 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
				influencer_package.save()
				
			if package_platform_9 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
				influencer_package.save()
				
			if package_platform_9 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
				influencer_package.save()
		if package_platform_10 is not None:
			package_content_type_10= request.POST.get('package_content_type_10')
			package_title_10= request.POST.get('package_title_10')
			package_description_10= request.POST.get('package_description_10')
			package_price_10= request.POST.get('package_price_10')
			if package_platform_10 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
				influencer_package.save()
			if package_platform_10 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
				influencer_package.save()
				
			if package_platform_10 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
				influencer_package.save()
				
			if package_platform_10 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
				influencer_package.save()
				
			if package_platform_10 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
				influencer_package.save()
				
			if package_platform_10 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
				influencer_package.save()
		if package_platform_11 is not None:
			package_content_type_11= request.POST.get('package_content_type_11')
			package_title_11= request.POST.get('package_title_11')
			package_description_11= request.POST.get('package_description_11')
			package_price_11= request.POST.get('package_price_11')
			if package_platform_11 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
				influencer_package.save()
			if package_platform_11 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
				influencer_package.save()
				
			if package_platform_11 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
				influencer_package.save()
				
			if package_platform_11 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
				influencer_package.save()
				
			if package_platform_11 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
				influencer_package.save()
				
			if package_platform_11 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
				influencer_package.save()
		if package_platform_12 is not None:
			package_content_type_12= request.POST.get('package_content_type_12')
			package_title_12= request.POST.get('package_title_12')
			package_description_12= request.POST.get('package_description_12')
			package_price_12= request.POST.get('package_price_12')
			if package_platform_12 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
				influencer_package.save()
			if package_platform_12 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
				influencer_package.save()
				
			if package_platform_12 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
				influencer_package.save()
				
			if package_platform_12 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
				influencer_package.save()
				
			if package_platform_12 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
				influencer_package.save()
				
			if package_platform_12 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
				influencer_package.save()
		if package_platform_13 is not None:
			package_content_type_13= request.POST.get('package_content_type_13')
			package_title_13= request.POST.get('package_title_13')
			package_description_13= request.POST.get('package_description_13')
			package_price_13= request.POST.get('package_price_13')
			if package_platform_13 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
				influencer_package.save()
			if package_platform_13 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
				influencer_package.save()
				
			if package_platform_13 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
				influencer_package.save()
				
			if package_platform_13 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
				influencer_package.save()
				
			if package_platform_13 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
				influencer_package.save()
				
			if package_platform_13 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
				influencer_package.save()
		if package_platform_14 is not None:
			package_content_type_14= request.POST.get('package_content_type_14')
			package_title_14= request.POST.get('package_title_14')
			package_description_14= request.POST.get('package_description_14')
			package_price_14= request.POST.get('package_price_14')
			if package_platform_14 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
				influencer_package.save()
			if package_platform_14 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
				influencer_package.save()
				
			if package_platform_14 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
				influencer_package.save()
				
			if package_platform_14 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
				influencer_package.save()
				
			if package_platform_14 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
				influencer_package.save()
				
			if package_platform_14 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
				influencer_package.save()
		if package_platform_15 is not None:
			package_content_type_15= request.POST.get('package_content_type_15')
			package_title_15= request.POST.get('package_title_15')
			package_description_15= request.POST.get('package_description_15')
			package_price_15= request.POST.get('package_price_15')
			if package_platform_15 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
				influencer_package.save()
			if package_platform_15 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
				influencer_package.save()
				
			if package_platform_15 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
				influencer_package.save()
				
			if package_platform_15 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
				influencer_package.save()
				
			if package_platform_15 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
				influencer_package.save()
				
			if package_platform_15 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
				influencer_package.save()
		if package_platform_16 is not None:
			package_content_type_16= request.POST.get('package_content_type_16')
			package_title_16= request.POST.get('package_title_16')
			package_description_16= request.POST.get('package_description_16')
			package_price_16= request.POST.get('package_price_16')
			if package_platform_16 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
				influencer_package.save()
			if package_platform_16 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
				influencer_package.save()
				
			if package_platform_16 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
				influencer_package.save()
				
			if package_platform_16 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
				influencer_package.save()
				
			if package_platform_16 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
				influencer_package.save()
				
			if package_platform_16 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
				influencer_package.save()
		if package_platform_17 is not None:
			package_content_type_17= request.POST.get('package_content_type_17')
			package_title_17= request.POST.get('package_title_17')
			package_description_17= request.POST.get('package_description_17')
			package_price_17= request.POST.get('package_price_17')
			if package_platform_17 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
				influencer_package.save()
			if package_platform_17 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
				influencer_package.save()
				
			if package_platform_17 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
				influencer_package.save()
				
			if package_platform_17 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
				influencer_package.save()
				
			if package_platform_17 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
				influencer_package.save()
				
			if package_platform_17 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
				influencer_package.save()
		if package_platform_18 is not None:
			package_content_type_18= request.POST.get('package_content_type_18')
			package_title_18= request.POST.get('package_title_18')
			package_description_18= request.POST.get('package_description_18')
			package_price_18= request.POST.get('package_price_18')
			if package_platform_18 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
				influencer_package.save()
			if package_platform_18 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
				influencer_package.save()
				
			if package_platform_18 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
				influencer_package.save()
				
			if package_platform_18 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
				influencer_package.save()
				
			if package_platform_18 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
				influencer_package.save()
				
			if package_platform_18 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
				influencer_package.save()
		if package_platform_19 is not None:
			package_content_type_19= request.POST.get('package_content_type_19')
			package_title_19= request.POST.get('package_title_19')
			package_description_19= request.POST.get('package_description_19')
			package_price_19= request.POST.get('package_price_19')
			if package_platform_19 == '1':
				print('Inside package platform::::::::::::::::::::::')
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
				influencer_package.save()
			if package_platform_19 == '2':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
				influencer_package.save()
				
			if package_platform_19 == '3':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
				influencer_package.save()
				
			if package_platform_19 == '4':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
				influencer_package.save()
				
			if package_platform_19 == '5':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
				influencer_package.save()
				
			if package_platform_19 == '6':
				influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
				influencer_package.save()
		# Form No 8 End
		# _________________________________________________________________
		# Form No 9 Faqs
		faq_question_0= request.POST.get('faq_question_0')
		faq_answer_0= request.POST.get('faq_answer_0')
		faq_question_1= request.POST.get('faq_question_1')
		faq_answer_1= request.POST.get('faq_answer_1')
		faq_question_2= request.POST.get('faq_question_2')
		faq_answer_2= request.POST.get('faq_answer_2')
		faq_question_3= request.POST.get('faq_question_3')
		faq_answer_3= request.POST.get('faq_answer_3')
		faq_question_4= request.POST.get('faq_question_4')
		faq_answer_4= request.POST.get('faq_answer_4')
		faq_question_5= request.POST.get('faq_question_5')
		faq_answer_5= request.POST.get('faq_answer_5')
		faq_question_6= request.POST.get('faq_question_6')
		faq_answer_6= request.POST.get('faq_answer_6')
		faq_question_7= request.POST.get('faq_question_7')
		faq_answer_7= request.POST.get('faq_answer_7')
		faq_question_8= request.POST.get('faq_question_8')
		faq_answer_8= request.POST.get('faq_answer_8')
		faq_question_9= request.POST.get('faq_question_9')
		faq_answer_9= request.POST.get('faq_answer_9')
		if ((faq_question_0 != "") and  (faq_answer_0 != "")):
			print('In if statement of FAqs 1########')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_0, faq_answer=faq_answer_0)
			Influencer_faq.save()
		if ((faq_question_1 != "") and  (faq_answer_1 != "")):
			print('In if statement of FAqs2')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_1, faq_answer=faq_answer_1)
			Influencer_faq.save()
		if ((faq_question_2 != "") and  (faq_answer_2 != "")):
			print('In if statement of FAqs3')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_2, faq_answer=faq_answer_2)
			Influencer_faq.save()
		if ((faq_question_3 != "") and  (faq_answer_3 != "")):
			print('In if statement of FAqs4')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_3, faq_answer=faq_answer_3)	
			Influencer_faq.save()
		if ((faq_question_4 != "") and  (faq_answer_4 != "")):
			print('In if statement of FAqs5')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_4, faq_answer=faq_answer_4)	
			Influencer_faq.save()
		if ((faq_question_5 != "") and  (faq_answer_5 != "")):
			print('In if statement of FAqs')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_5, faq_answer=faq_answer_5)	
			Influencer_faq.save()
		if ((faq_question_6 != "") and  (faq_answer_6 != "")):
			print('In if statement of FAqs')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_6, faq_answer=faq_answer_6)	
			Influencer_faq.save()
		if ((faq_question_7 != "") and  (faq_answer_7 != "")):
			print('In if statement of FAqs')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_7, faq_answer=faq_answer_7)	
			Influencer_faq.save()
		if ((faq_question_8 != "") and  (faq_answer_8 != "")):
			print('In if statement of FAqs')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_8, faq_answer=faq_answer_8)	
			Influencer_faq.save()
		if ((faq_question_9 != "") and  (faq_answer_9 != "")):
			print('In if statement of FAqs')
			Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_9, faq_answer=faq_answer_9)	
			Influencer_faq.save()
		
		
		
		
		
		
		
		
		
		
		
		context={'influencer_username_3': influencer_username_3}
		return render(request,'User/login.html', context)
	


def influencer_profile(request):
	username = None
	try:
		if request.user.is_authenticated:
			print("User is logged in :)")
			username= request.user.username
			joined_influencer=JoinInfluencer.objects.get(influencer_username=username)
			package_influencer=InfluencerPackage.objects.filter(influencer_username__influencer_username=username)
			faq_influencer=InfluencerFaq.objects.filter(influencer_username__influencer_username=username)
			print('joined_influencer::::::::::',joined_influencer)
			context={'joined_influencer': joined_influencer, 'package_influencer': package_influencer, 'faq_influencer': faq_influencer}
			return render(request, 'User/influencer_profile.html', context)
		else:
			print("User is not logged in :(")
			# return redirect(request, 'User/influencer_profile.html')
	except Exception as e:
			# messages.success(request, 'Superuser logged in')
			return redirect('home')


def influencer_profile_edit(request):
	try:
		if request.user.is_authenticated:
			print("User is logged in :)")
			username= request.user.username
			influencer=User.objects.get(username= username)
			
			joined_influencer=JoinInfluencer.objects.get(influencer_username=username)
			package_influencer=InfluencerPackage.objects.filter(influencer_username__influencer_username=username)
			faq_influencer=InfluencerFaq.objects.filter(influencer_username__influencer_username=username)
			print('joined_influencer::::::::::',joined_influencer)
			if request.method == 'POST':
				print('influencer firstname', influencer.first_name)
				influencer_fullname= request.POST.get('influencer_fullname')
				influencer_location= request.POST.get('influencer_location')
				influencer_title= request.POST.get('influencer_title')
				influencer_description= request.POST.get('influencer_description')
				influencer_gender= request.POST.get('influencer_gender')
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
				
				
				if influencer_fullname != "":
					print('#####################################')
					print('influencer_fullname edit:::',influencer_fullname)
					influencer.first_name=influencer_fullname
					influencer.save()
					joined_influencer.full_name=influencer_fullname
					joined_influencer.save()
				if influencer_location!= "":
					joined_influencer.location=influencer_location
					joined_influencer.save()
				if influencer_title!= "":
					joined_influencer.title_influencer=influencer_title
					joined_influencer.save()
				if influencer_description!= "":
					joined_influencer.description_influencer=influencer_description
					joined_influencer.save()
				if influencer_gender!= "":
					joined_influencer.gender_influencer=influencer_gender
					joined_influencer.save()
				if instagram_username!= "":
					joined_influencer.instagram_username=instagram_username
					joined_influencer.instagram_followers=instagram_followers
					joined_influencer.save()
				if tiktok_username!= "":
					joined_influencer.tiktok_username=tiktok_username
					joined_influencer.tiktok_followers=tiktok_followers
					joined_influencer.save()
				if youtube_username!= "":
					joined_influencer.youtube_url=youtube_username
					joined_influencer.youtube_followers=youtube_followers
					joined_influencer.save()
				if twitter_username!= "":
					joined_influencer.twitter_username=twitter_username
					joined_influencer.twitter_followers=twitter_followers
					joined_influencer.save()
				if twitch_username!= "":
					joined_influencer.twitch_username=twitch_username
					joined_influencer.twitch_followers=twitch_followers
					joined_influencer.save()
				if website!= "":
					joined_influencer.instagram_username=website
					
					joined_influencer.save()
				return redirect('influencer_profile_edit')
			context={'joined_influencer': joined_influencer, 'package_influencer': package_influencer, 'faq_influencer': faq_influencer}
			return render(request, 'User/infl_profile_edit.html', context)
				
			
		else:
			print("User is not logged in :(")
			# return redirect(request, 'User/influencer_profile.html')
	except Exception as e:
			# messages.success(request, 'Superuser logged in')
			print(e)
	return render(request, 'User/infl_profile_edit.html')
