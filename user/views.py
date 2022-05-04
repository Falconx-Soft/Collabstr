from multiprocessing import context
import profile
from urllib.parse import uses_netloc
from django.http import HttpResponse
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
import stripe

# from .models import join_influencer
stripe.api_key= 'sk_test_51KhIAhGppnrRkU6FOSJWqqiDXogb03Zh0gF9tEg9ov0aCIHdPsN4ptPDlEM5pkRAzuYv30LRiwSG9e2bOvnr5rZH00Wv7Ifh6t'

# Create your views here.
# @login_required(login_url='login')
def home(request):
	all_influencer=JoinInfluencer.objects.all()
	all_packages=InfluencerPackage.objects.all()
	print('all_packages___________________',all_packages)
	print('all_packages_________________0000__',all_packages[0])
	context= {'all_influencer': all_influencer,'all_packages':all_packages}

	return render(request,'User/home.html', context)

def ater_brand_signup(request):

	return render(request,'User/after_brand_signup.html')

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
		brand_fullname= request.POST.get('brand_fullname')
		brand_name= request.POST.get('brand_name')
		brand_email= request.POST.get('brand_email')
		brand_password= request.POST.get('brand_password')
		brand_website= request.POST.get('brand_website')
		brand_instagram= request.POST.get('brand_instagram')
		brand_tiktok= request.POST.get('brand_tiktok')
		brand_youtube= request.POST.get('brand_youtube')
		try:
			if User.objects.filter(email=brand_email):
				messages.success(request, 'Email is already in use')
				return redirect(request, 'signup.html')
			
		
			user_obj= User(username=brand_fullname, email=brand_email, is_brand= True)
			user_obj.set_password(brand_password)
			user_obj.save()
			join_brand_obj= JoinBrand.objects.create(full_name=brand_fullname, brand_name=brand_name, brand_email=brand_email, brand_website= brand_website, brand_instagram=brand_instagram, brand_tiktok=brand_tiktok, brand_youtube=brand_youtube)
			join_brand_obj.save()
			is_brand_obj= BrandorInfluencer.objects.create(user=user_obj, brand=True)
			is_brand_obj.save()
			user = authenticate(username=brand_fullname, password=brand_password)
			login(request, user)
			return redirect('after_brand_signup')
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
			print('Influencer username:::::@@@@',influencer_username)
			if JoinInfluencer.objects.filter(influencer_username=influencer_username):
				messages.success(request, 'Username Not Available')
				return redirect(request, 'join_as_influencer.html')
			else:

			
				influencer_obj2= JoinInfluencer.objects.create(influencer_username= influencer_username)
				influencer_obj2.save()
				request.session['username_session'] = influencer_username
				username_session = request.session.get('username_session')
				print('join as inful username_session::::::@@@@',username_session)
				context= {'influencer_username': influencer_username}
				return render(request,'User/social_signup.html', context)
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
				is_brand_obj= BrandorInfluencer.objects.create(user=influencer, brand=False)
				is_brand_obj.save()
			context= {'influencer_username_2': influencer_username_2}
			return render(request,'User/join_influencer_profile.html', context)
		except Exception as e:
			print(e)
	return render(request,'User/create_your_page.html')



def join_influencer_profile(request):
	try:
		if request.method == 'POST':
			username_session = request.session.get('username_session')
			print('Fav username_session create page::::::@@@@',username_session)
			influencer_username_3= request.POST.get('influencer_username_3')
			# influencer=JoinInfluencer.objects.get(influencer_username= username_session)
			user_email_inful=request.user.email
			influencer=JoinInfluencer.objects.get(email_address= user_email_inful)
			location= request.POST.get('location_influencer')
			# title_influencer= request.POST.get('title_influencer')
			# description_influencer= request.POST.get('description_influencer')
			gender_influencer= request.POST.get('gender_influencer')
			print('gender_influencer_________________', gender_influencer)
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
			# niches= request.POST.get('niches_val')
			profile_image= request.FILES.get('profile_img')
			print('profile image join_________________', profile_image)
			all_image= request.FILES.getlist('img-files')
			print('all_________________', all_image)
			print('length of all_________________', len(all_image))
			print('image0 allimage&&&&&&&&&&&&&', all_image[0])
			cover_image= request.FILES.get('cover_image')
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
			# influencer.title_influencer=title_influencer
			# influencer.description_influencer=description_influencer
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
			if len(all_image) == 1:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
			if len(all_image) == 2:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
				influencer.image3=all_image[1]
			if len(all_image) == 3:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
				influencer.image3=all_image[1]
				influencer.image4=all_image[2]
			if len(all_image) == 4:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
				influencer.image3=all_image[1]
				influencer.image4=all_image[2]
				influencer.image5=all_image[3]

			if len(all_image) == 5:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
				influencer.image3=all_image[1]
				influencer.image4=all_image[2]
				influencer.image5=all_image[3]
			if len(all_image) == 6:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
				influencer.image3=all_image[1]
				influencer.image4=all_image[2]
				influencer.image5=all_image[3]
			if len(all_image) == 7:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
				influencer.image3=all_image[1]
				influencer.image4=all_image[2]
				influencer.image5=all_image[3]
			if len(all_image) == 8:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
				influencer.image3=all_image[1]
				influencer.image4=all_image[2]
				influencer.image5=all_image[3]
			if len(all_image) == 9:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
				influencer.image3=all_image[1]
				influencer.image4=all_image[2]
				influencer.image5=all_image[3]
			if len(all_image) == 10:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				influencer.cover_image=all_image[0]
				influencer.image3=all_image[1]
				influencer.image4=all_image[2]
				influencer.image5=all_image[3]
			if cover_image:

				influencer.cover_image=cover_image
			
			if img2:
				influencer.image3=img2
			if img3:
				influencer.image4=img3
			if img4:
				influencer.image5=img4
			# if "Lifestyle" in niches:
			# 	influencer.lifestyle= True
			# if "Fashion" in niches:
			# 	influencer.fashion= True
			# if "Beauty" in niches:
			# 	influencer.beauty= True
			
			# if "Health & Fitness" in niches:
			# 	influencer.health_fitness= True
			# if "Travel" in niches:
			# 	influencer.travel= True
			# if "Food & Drink" in niches:
			# 	influencer.food_drink= True
			# if "Model" in niches:
			# 	influencer.model= True
			# if "Comedy & Entertainment" in niches:
			# 	influencer.comedy_entertainment= True
			# if "Art & Photography" in niches:
			# 	influencer.art_photography= True
			
			# if "Music & Dance" in niches:
			# 	influencer.music_dance= True
			# if "Entrepreneur & Business" in niches:
			# 	influencer.entrepreneur_business= True
			# if "Family & Children" in niches:
			# 	influencer.family_children= True
			# if "Animals & Pets" in niches:
			# 	influencer.animals_pets= True
			# if "Athlete & Sports" in niches:
			# 	influencer.athlete_sports= True
			# if "Celebrity & Public Figure" in niches:
			# 	influencer.celebrity_public_pigure= True
			
			# if "Adventure & Outdoors" in niches:
			# 	influencer.adventure_outdoors= True
			# if "Actor" in niches:
			# 	influencer.actor= True
			# if "Education" in niches:
			# 	influencer.education= True
			# if "Gaming" in niches:
			# 	influencer.gaming= True
			# if "LGBTQ2" in niches:
			# 	influencer.lgbtq= True
			# if "Technology" in niches:
			# 	influencer.technology= True
			
			# if "Healthcare" in niches:
			# 	influencer.healthcare= True
			# if "Vegan" in niches:
			# 	influencer.vegan= True
			# if "Cannabis" in niches:
			# 	influencer.cannabis= True
			# if "Skilled Trades" in niches:
			# 	influencer.skilled_trades= True
			# if "Automotive" in niches:
			# 	influencer.automotive= True
			
			influencer.save()
			# ____________________________________________________________________________
			# Form no 8: all the packages
			if package_platform_0 is not None:
				package_content_type_0= request.POST.get('package_content_type_0')
				package_title_0= request.POST.get('package_title_0')
				package_description_0= request.POST.get('package_description_0')
				package_price_0= request.POST.get('package_price_0')
				package_price_0_int = int(package_price_0)
				if package_platform_0 == '1':
					print('Inside package platform::::::::::::::::::::::')
					influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Instagram' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0_int)
					influencer_package.save()
				if package_platform_0 == '2':
					influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'TikTok' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0_int)
					influencer_package.save()
					
				if package_platform_0 == '3':
					influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0_int)
					influencer_package.save()
					
				if package_platform_0 == '4':
					influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'YouTube' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0_int)
					influencer_package.save()
					
				if package_platform_0 == '5':
					influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitter' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0_int)
					influencer_package.save()
					
				if package_platform_0 == '6':
					influencer_package= InfluencerPackage.objects.create(influencer_username= influencer,choose_platform= 'Twitch' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0_int)
					influencer_package.save()
					
				
				print('##########################')
				print('package_content_type_0',package_content_type_0)
				print('**************************')
				print('package_title_0',package_title_0)
				print('**************************')
				print('package_description_0',package_description_0)
				print('**************************')
				print('package_price_0_int',package_price_0_int)
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
			# faq_question_0= request.POST.get('faq_question_0')
			# faq_answer_0= request.POST.get('faq_answer_0')
			# faq_question_1= request.POST.get('faq_question_1')
			# faq_answer_1= request.POST.get('faq_answer_1')
			# faq_question_2= request.POST.get('faq_question_2')
			# faq_answer_2= request.POST.get('faq_answer_2')
			# faq_question_3= request.POST.get('faq_question_3')
			# faq_answer_3= request.POST.get('faq_answer_3')
			# faq_question_4= request.POST.get('faq_question_4')
			# faq_answer_4= request.POST.get('faq_answer_4')
			# faq_question_5= request.POST.get('faq_question_5')
			# faq_answer_5= request.POST.get('faq_answer_5')
			# faq_question_6= request.POST.get('faq_question_6')
			# faq_answer_6= request.POST.get('faq_answer_6')
			# faq_question_7= request.POST.get('faq_question_7')
			# faq_answer_7= request.POST.get('faq_answer_7')
			# faq_question_8= request.POST.get('faq_question_8')
			# faq_answer_8= request.POST.get('faq_answer_8')
			# faq_question_9= request.POST.get('faq_question_9')
			# faq_answer_9= request.POST.get('faq_answer_9')
			# if ((faq_question_0 != "") and  (faq_answer_0 != "")):
			# 	print('In if statement of FAqs 1########')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_0, faq_answer=faq_answer_0)
			# 	Influencer_faq.save()
			# if ((faq_question_1 != "") and  (faq_answer_1 != "")):
			# 	print('In if statement of FAqs2')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_1, faq_answer=faq_answer_1)
			# 	Influencer_faq.save()
			# if ((faq_question_2 != "") and  (faq_answer_2 != "")):
			# 	print('In if statement of FAqs3')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_2, faq_answer=faq_answer_2)
			# 	Influencer_faq.save()
			# if ((faq_question_3 != "") and  (faq_answer_3 != "")):
			# 	print('In if statement of FAqs4')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_3, faq_answer=faq_answer_3)	
			# 	Influencer_faq.save()
			# if ((faq_question_4 != "") and  (faq_answer_4 != "")):
			# 	print('In if statement of FAqs5')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_4, faq_answer=faq_answer_4)	
			# 	Influencer_faq.save()
			# if ((faq_question_5 != "") and  (faq_answer_5 != "")):
			# 	print('In if statement of FAqs')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_5, faq_answer=faq_answer_5)	
			# 	Influencer_faq.save()
			# if ((faq_question_6 != "") and  (faq_answer_6 != "")):
			# 	print('In if statement of FAqs')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_6, faq_answer=faq_answer_6)	
			# 	Influencer_faq.save()
			# if ((faq_question_7 != "") and  (faq_answer_7 != "")):
			# 	print('In if statement of FAqs')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_7, faq_answer=faq_answer_7)	
			# 	Influencer_faq.save()
			# if ((faq_question_8 != "") and  (faq_answer_8 != "")):
			# 	print('In if statement of FAqs')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_8, faq_answer=faq_answer_8)	
			# 	Influencer_faq.save()
			# if ((faq_question_9 != "") and  (faq_answer_9 != "")):
			# 	print('In if statement of FAqs')
			# 	Influencer_faq=InfluencerFaq.objects.create(influencer_username=influencer, faq_question=faq_question_9, faq_answer=faq_answer_9)	
			# 	Influencer_faq.save()
			
			
			
			
			
			
			
			
			
			
			
			context={'influencer_username_3': influencer_username_3}
			return redirect('home')
		
	except Exception as e:
		messages.success(request, 'Something is wrong')
		return redirect('home')


def influencer_profile(request):
	username = None

	try:

		if request.user.is_authenticated:
			print("User is logged in :)")
			user_email_inful=request.user.email
			username= request.user.username
			is_brand=BrandorInfluencer.objects.get(user__username=username)
			is_brand_value= is_brand.brand
			print("User is is_brand___________________________--- :)", is_brand_value)
			print("User is is_brand_value--------------------------- :)", is_brand)
			if is_brand_value:
				return redirect('/brandprofile/')
			joined_influencer=JoinInfluencer.objects.get(email_address=user_email_inful)
			username_inful=joined_influencer.influencer_username
			print('joined_influencer::::::::::',username_inful)
			package_influencer=InfluencerPackage.objects.filter(influencer_username__influencer_username=username_inful)
			faq_influencer=InfluencerFaq.objects.filter(influencer_username__influencer_username=username_inful)
			edit_portfolio=EditPortfolioImages.objects.filter(influencer_username__influencer_username=username_inful)
			print('joined_influencer::::::::::',joined_influencer)
			context={'joined_influencer': joined_influencer, 'package_influencer': package_influencer, 'faq_influencer': faq_influencer, 'edit_portfolio':edit_portfolio}
			return render(request, 'User/influencer_profile.html', context)
		else:
			print("User is not logged in :(")
			# return redirect(request, 'User/influencer_profile.html')
	except Exception as e:
			messages.success(request, 'oops there was problem')
			return redirect('home')


def influencer_profile_edit(request):
	try:
		if request.user.is_authenticated:
			print("User is logged in :)")
			username= request.user.email
			influencer=User.objects.get(email= username)
			
			joined_influencer=JoinInfluencer.objects.get(email_address=username)
			username_inful=joined_influencer.influencer_username
			package_influencer=InfluencerPackage.objects.filter(influencer_username__influencer_username=username_inful)
			faq_influencer=InfluencerFaq.objects.filter(influencer_username__influencer_username=username_inful)
			print('joined_influencer edit::::::::::',joined_influencer)
			if request.method == 'POST':
				print('influencer firstname', influencer.first_name)
				influencer_fullname= request.POST.get('influencer_fullname')
				influencer_location= request.POST.get('influencer_location')
				# influencer_title= request.POST.get('influencer_title')
				# influencer_description= request.POST.get('influencer_description')
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
				profile_img= request.FILES.get('profile_img_edit')
				print('profile image edit_____', profile_img)
				cover_image= request.FILES.get('cover_image')
				img2= request.FILES.get('img2')
				img3= request.FILES.get('img3')
				img4= request.FILES.get('img4')

				package_platform_0= request.POST.get('package_category_0')
				package_platform_1= request.POST.get('package_category_1')
				package_platform_2= request.POST.get('package_category_2')
				package_platform_3= request.POST.get('package_category_3')
				package_platform_4= request.POST.get('package_category_4')
				package_platform_5= request.POST.get('package_category_5')
				package_platform_6= request.POST.get('package_category_6')
				package_platform_7= request.POST.get('package_category_7')
				package_platform_8= request.POST.get('package_category_8')
				package_platform_9= request.POST.get('package_category_9')
				package_platform_10= request.POST.get('package_category_10')
				package_platform_11= request.POST.get('package_category_11')
				package_platform_12= request.POST.get('package_category_12')
				package_platform_13= request.POST.get('package_category_13')
				package_platform_14= request.POST.get('package_category_14')
				package_platform_15= request.POST.get('package_category_15')
				package_platform_16= request.POST.get('package_category_16')
				package_platform_17= request.POST.get('package_category_17')
				package_platform_18= request.POST.get('package_category_18')
				package_platform_19= request.POST.get('package_category_19')
				
				
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
				# if influencer_title!= "":
				# 	joined_influencer.title_influencer=influencer_title
				# 	joined_influencer.save()
				# if influencer_description!= "":
				# 	joined_influencer.description_influencer=influencer_description
				# 	joined_influencer.save()
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
				
				
				
				# _________________________________________images
				if profile_img:
					print('^^^^^^^ Inside 1 ^^^^^^^^^^^^^^')
					joined_influencer.profile_image=profile_img
					
					joined_influencer.save()
				if cover_image:
					print('^^^^^^^ Inside 2 ^^^^^^^^^^^^^^')
					joined_influencer.cover_image=cover_image
					
					joined_influencer.save()
				if img2:
					print('^^^^^^^ Inside 3 ^^^^^^^^^^^^^^')
					joined_influencer.image3=img2
					
					joined_influencer.save()
				if img3:
					print('^^^^^^^ Inside 4 ^^^^^^^^^^^^^^')
					joined_influencer.image4=img3
					
					joined_influencer.save()
				if img4:
					print('^^^^^^^ Inside 5 ^^^^^^^^^^^^^^')
					joined_influencer.image5=img4
					
					joined_influencer.save()
				# __________________________________ Packages
				if package_platform_0 is not None:
					package_content_type_0= request.POST.get('package_content_type_0')
					package_title_0= request.POST.get('package_title_0')
					package_description_0= request.POST.get('package_description_0')
					package_price_0= request.POST.get('package_price_0')
					if package_platform_0 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
						influencer_package.save()
					if package_platform_0 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
						influencer_package.save()
						
					if package_platform_0 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
						influencer_package.save()
						
					if package_platform_0 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
						influencer_package.save()
						
					if package_platform_0 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
						influencer_package.save()
						
					if package_platform_0 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_0,package_offering=package_title_0,package_include=package_description_0,package_price=package_price_0)
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
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
						influencer_package.save()
					if package_platform_1 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
						influencer_package.save()
						
					if package_platform_1 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
						influencer_package.save()
						
					if package_platform_1 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
						influencer_package.save()
						
					if package_platform_1 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
						influencer_package.save()
						
					if package_platform_1 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_1,package_offering=package_title_1,package_include=package_description_1,package_price=package_price_1)
						influencer_package.save()
								
				if package_platform_2 is not None:
					package_content_type_2= request.POST.get('package_content_type_2')
					package_title_2= request.POST.get('package_title_2')
					package_description_2= request.POST.get('package_description_2')
					package_price_2= request.POST.get('package_price_2')
					if package_platform_2 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
						influencer_package.save()
					if package_platform_2 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
						influencer_package.save()
						
					if package_platform_2 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
						influencer_package.save()
						
					if package_platform_2 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
						influencer_package.save()
						
					if package_platform_2 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
						influencer_package.save()
						
					if package_platform_2 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_2,package_offering=package_title_2,package_include=package_description_2,package_price=package_price_2)
						influencer_package.save()
				if package_platform_3 is not None:
					package_content_type_3= request.POST.get('package_content_type_3')
					package_title_3= request.POST.get('package_title_3')
					package_description_3= request.POST.get('package_description_3')
					package_price_3= request.POST.get('package_price_3')
					if package_platform_3 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
						influencer_package.save()
					if package_platform_3 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
						influencer_package.save()
						
					if package_platform_3 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
						influencer_package.save()
						
					if package_platform_3 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
						influencer_package.save()
						
					if package_platform_3 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
						influencer_package.save()
						
					if package_platform_3 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_3,package_offering=package_title_3,package_include=package_description_3,package_price=package_price_3)
						influencer_package.save()	
				if package_platform_4 is not None:
					package_content_type_4= request.POST.get('package_content_type_4')
					package_title_4= request.POST.get('package_title_4')
					package_description_4= request.POST.get('package_description_4')
					package_price_4= request.POST.get('package_price_4')
					if package_platform_4 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
						influencer_package.save()
					if package_platform_4 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
						influencer_package.save()
						
					if package_platform_4 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
						influencer_package.save()
						
					if package_platform_4 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
						influencer_package.save()
						
					if package_platform_4 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
						influencer_package.save()
						
					if package_platform_4 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_4,package_offering=package_title_4,package_include=package_description_4,package_price=package_price_4)
						influencer_package.save()
				if package_platform_5 is not None:
					package_content_type_5= request.POST.get('package_content_type_5')
					package_title_5= request.POST.get('package_title_5')
					package_description_5= request.POST.get('package_description_5')
					package_price_5= request.POST.get('package_price_5')
					if package_platform_5 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
						influencer_package.save()
					if package_platform_5 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
						influencer_package.save()
						
					if package_platform_5 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
						influencer_package.save()
						
					if package_platform_5 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
						influencer_package.save()
						
					if package_platform_5 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
						influencer_package.save()
						
					if package_platform_5 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_5,package_offering=package_title_5,package_include=package_description_5,package_price=package_price_5)
						influencer_package.save()
				if package_platform_6 is not None:
					package_content_type_6= request.POST.get('package_content_type_6')
					package_title_6= request.POST.get('package_title_6')
					package_description_6= request.POST.get('package_description_6')
					package_price_6= request.POST.get('package_price_6')
					if package_platform_6 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
						influencer_package.save()
					if package_platform_6 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
						influencer_package.save()
						
					if package_platform_6 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
						influencer_package.save()
						
					if package_platform_6 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
						influencer_package.save()
						
					if package_platform_6 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
						influencer_package.save()
						
					if package_platform_6 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_6,package_offering=package_title_6,package_include=package_description_6,package_price=package_price_6)
						influencer_package.save()	
				if package_platform_7 is not None:
					package_content_type_7= request.POST.get('package_content_type_7')
					package_title_7= request.POST.get('package_title_7')
					package_description_7= request.POST.get('package_description_7')
					package_price_7= request.POST.get('package_price_7')
					if package_platform_7 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
						influencer_package.save()
					if package_platform_7 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
						influencer_package.save()
						
					if package_platform_7 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
						influencer_package.save()
						
					if package_platform_7 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
						influencer_package.save()
						
					if package_platform_7 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
						influencer_package.save()
						
					if package_platform_7 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_7,package_offering=package_title_7,package_include=package_description_7,package_price=package_price_7)
						influencer_package.save()
				if package_platform_8 is not None:
					package_content_type_8= request.POST.get('package_content_type_8')
					package_title_8= request.POST.get('package_title_8')
					package_description_8= request.POST.get('package_description_8')
					package_price_8= request.POST.get('package_price_8')
					if package_platform_8 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
						influencer_package.save()
					if package_platform_8 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
						influencer_package.save()
						
					if package_platform_8 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
						influencer_package.save()
						
					if package_platform_8 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
						influencer_package.save()
						
					if package_platform_8 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
						influencer_package.save()
						
					if package_platform_8 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_8,package_offering=package_title_8,package_include=package_description_8,package_price=package_price_8)
						influencer_package.save()
				if package_platform_9 is not None:
					package_content_type_9= request.POST.get('package_content_type_9')
					package_title_9= request.POST.get('package_title_9')
					package_description_9= request.POST.get('package_description_9')
					package_price_9= request.POST.get('package_price_9')
					if package_platform_9 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
						influencer_package.save()
					if package_platform_9 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
						influencer_package.save()
						
					if package_platform_9 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
						influencer_package.save()
						
					if package_platform_9 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
						influencer_package.save()
						
					if package_platform_9 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
						influencer_package.save()
						
					if package_platform_9 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_9,package_offering=package_title_9,package_include=package_description_9,package_price=package_price_9)
						influencer_package.save()
				if package_platform_10 is not None:
					package_content_type_10= request.POST.get('package_content_type_10')
					package_title_10= request.POST.get('package_title_10')
					package_description_10= request.POST.get('package_description_10')
					package_price_10= request.POST.get('package_price_10')
					if package_platform_10 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
						influencer_package.save()
					if package_platform_10 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
						influencer_package.save()
						
					if package_platform_10 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
						influencer_package.save()
						
					if package_platform_10 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
						influencer_package.save()
						
					if package_platform_10 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
						influencer_package.save()
						
					if package_platform_10 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_10,package_offering=package_title_10,package_include=package_description_10,package_price=package_price_10)
						influencer_package.save()
				if package_platform_11 is not None:
					package_content_type_11= request.POST.get('package_content_type_11')
					package_title_11= request.POST.get('package_title_11')
					package_description_11= request.POST.get('package_description_11')
					package_price_11= request.POST.get('package_price_11')
					if package_platform_11 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
						influencer_package.save()
					if package_platform_11 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
						influencer_package.save()
						
					if package_platform_11 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
						influencer_package.save()
						
					if package_platform_11 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
						influencer_package.save()
						
					if package_platform_11 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
						influencer_package.save()
						
					if package_platform_11 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_11,package_offering=package_title_11,package_include=package_description_11,package_price=package_price_11)
						influencer_package.save()
				if package_platform_12 is not None:
					package_content_type_12= request.POST.get('package_content_type_12')
					package_title_12= request.POST.get('package_title_12')
					package_description_12= request.POST.get('package_description_12')
					package_price_12= request.POST.get('package_price_12')
					if package_platform_12 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
						influencer_package.save()
					if package_platform_12 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
						influencer_package.save()
						
					if package_platform_12 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
						influencer_package.save()
						
					if package_platform_12 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
						influencer_package.save()
						
					if package_platform_12 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
						influencer_package.save()
						
					if package_platform_12 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_12,package_offering=package_title_12,package_include=package_description_12,package_price=package_price_12)
						influencer_package.save()
				if package_platform_13 is not None:
					package_content_type_13= request.POST.get('package_content_type_13')
					package_title_13= request.POST.get('package_title_13')
					package_description_13= request.POST.get('package_description_13')
					package_price_13= request.POST.get('package_price_13')
					if package_platform_13 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
						influencer_package.save()
					if package_platform_13 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
						influencer_package.save()
						
					if package_platform_13 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
						influencer_package.save()
						
					if package_platform_13 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
						influencer_package.save()
						
					if package_platform_13 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
						influencer_package.save()
						
					if package_platform_13 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_13,package_offering=package_title_13,package_include=package_description_13,package_price=package_price_13)
						influencer_package.save()
				if package_platform_14 is not None:
					package_content_type_14= request.POST.get('package_content_type_14')
					package_title_14= request.POST.get('package_title_14')
					package_description_14= request.POST.get('package_description_14')
					package_price_14= request.POST.get('package_price_14')
					if package_platform_14 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
						influencer_package.save()
					if package_platform_14 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
						influencer_package.save()
						
					if package_platform_14 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
						influencer_package.save()
						
					if package_platform_14 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
						influencer_package.save()
						
					if package_platform_14 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
						influencer_package.save()
						
					if package_platform_14 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_14,package_offering=package_title_14,package_include=package_description_14,package_price=package_price_14)
						influencer_package.save()
				if package_platform_15 is not None:
					package_content_type_15= request.POST.get('package_content_type_15')
					package_title_15= request.POST.get('package_title_15')
					package_description_15= request.POST.get('package_description_15')
					package_price_15= request.POST.get('package_price_15')
					if package_platform_15 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
						influencer_package.save()
					if package_platform_15 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
						influencer_package.save()
						
					if package_platform_15 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
						influencer_package.save()
						
					if package_platform_15 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
						influencer_package.save()
						
					if package_platform_15 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
						influencer_package.save()
						
					if package_platform_15 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_15,package_offering=package_title_15,package_include=package_description_15,package_price=package_price_15)
						influencer_package.save()
				if package_platform_16 is not None:
					package_content_type_16= request.POST.get('package_content_type_16')
					package_title_16= request.POST.get('package_title_16')
					package_description_16= request.POST.get('package_description_16')
					package_price_16= request.POST.get('package_price_16')
					if package_platform_16 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
						influencer_package.save()
					if package_platform_16 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
						influencer_package.save()
						
					if package_platform_16 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
						influencer_package.save()
						
					if package_platform_16 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
						influencer_package.save()
						
					if package_platform_16 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
						influencer_package.save()
						
					if package_platform_16 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_16,package_offering=package_title_16,package_include=package_description_16,package_price=package_price_16)
						influencer_package.save()
				if package_platform_17 is not None:
					package_content_type_17= request.POST.get('package_content_type_17')
					package_title_17= request.POST.get('package_title_17')
					package_description_17= request.POST.get('package_description_17')
					package_price_17= request.POST.get('package_price_17')
					if package_platform_17 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
						influencer_package.save()
					if package_platform_17 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
						influencer_package.save()
						
					if package_platform_17 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
						influencer_package.save()
						
					if package_platform_17 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
						influencer_package.save()
						
					if package_platform_17 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
						influencer_package.save()
						
					if package_platform_17 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_17,package_offering=package_title_17,package_include=package_description_17,package_price=package_price_17)
						influencer_package.save()
				if package_platform_18 is not None:
					package_content_type_18= request.POST.get('package_content_type_18')
					package_title_18= request.POST.get('package_title_18')
					package_description_18= request.POST.get('package_description_18')
					package_price_18= request.POST.get('package_price_18')
					if package_platform_18 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
						influencer_package.save()
					if package_platform_18 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
						influencer_package.save()
						
					if package_platform_18 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
						influencer_package.save()
						
					if package_platform_18 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
						influencer_package.save()
						
					if package_platform_18 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
						influencer_package.save()
						
					if package_platform_18 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_18,package_offering=package_title_18,package_include=package_description_18,package_price=package_price_18)
						influencer_package.save()
				if package_platform_19 is not None:
					package_content_type_19= request.POST.get('package_content_type_19')
					package_title_19= request.POST.get('package_title_19')
					package_description_19= request.POST.get('package_description_19')
					package_price_19= request.POST.get('package_price_19')
					if package_platform_19 == '1':
						print('Inside package platform::::::::::::::::::::::')
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Instagram' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
						influencer_package.save()
					if package_platform_19 == '2':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'TikTok' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
						influencer_package.save()
						
					if package_platform_19 == '3':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'User Generated Content' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
						influencer_package.save()
						
					if package_platform_19 == '4':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'YouTube' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
						influencer_package.save()
						
					if package_platform_19 == '5':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitter' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
						influencer_package.save()
						
					if package_platform_19 == '6':
						influencer_package= InfluencerPackage.objects.create(influencer_username= joined_influencer,choose_platform= 'Twitch' , content_category=package_content_type_19,package_offering=package_title_19,package_include=package_description_19,package_price=package_price_19)
						influencer_package.save()
				# Form No 8 End
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
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_0, faq_answer=faq_answer_0)
					Influencer_faq.save()
				if ((faq_question_1 != "") and  (faq_answer_1 != "")):
					print('In if statement of FAqs2')
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_1, faq_answer=faq_answer_1)
					Influencer_faq.save()
				if ((faq_question_2 != "") and  (faq_answer_2 != "")):
					print('In if statement of FAqs3')
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_2, faq_answer=faq_answer_2)
					Influencer_faq.save()
				if ((faq_question_3 != "") and  (faq_answer_3 != "")):
					print('In if statement of FAqs4')
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_3, faq_answer=faq_answer_3)	
					Influencer_faq.save()
				if ((faq_question_4 != "") and  (faq_answer_4 != "")):
					print('In if statement of FAqs5')
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_4, faq_answer=faq_answer_4)	
					Influencer_faq.save()
				if ((faq_question_5 != "") and  (faq_answer_5 != "")):
					print('In if statement of FAqs')
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_5, faq_answer=faq_answer_5)	
					Influencer_faq.save()
				if ((faq_question_6 != "") and  (faq_answer_6 != "")):
					print('In if statement of FAqs')
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_6, faq_answer=faq_answer_6)	
					Influencer_faq.save()
				if ((faq_question_7 != "") and  (faq_answer_7 != "")):
					print('In if statement of FAqs')
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_7, faq_answer=faq_answer_7)	
					Influencer_faq.save()
				if ((faq_question_8 != "") and  (faq_answer_8 != "")):
					print('In if statement of FAqs')
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_8, faq_answer=faq_answer_8)	
					Influencer_faq.save()
				if ((faq_question_9 != "") and  (faq_answer_9 != "")):
					print('In if statement of FAqs')
					Influencer_faq=InfluencerFaq.objects.create(influencer_username=joined_influencer, faq_question=faq_question_9, faq_answer=faq_answer_9)	
					Influencer_faq.save()
				


				# portfolio images
				portfolio_pic= request.FILES.getlist('portfolio_pic')
				print('portfolio_pic:::::::::-------------------------------:', portfolio_pic)
				for image in portfolio_pic:
					edit_port_folio= EditPortfolioImages.objects.create(influencer_username=joined_influencer, image_url=image)
					edit_port_folio.save()
				# print('portfolio_pic::::::::::', portfolio_pic)
				# image_portfolio= request.POST.get('portfolio_input') 
				# print('image_portfolio::::::::::', image_portfolio) 
				# images_portfolio_url = image_portfolio.split(",")
				# length_images= len(images_portfolio_url)
				# print('images_portfolio_url************************',images_portfolio_url[0])
				# for i in range(1, length_images):
				# 	edit_port_folio= EditPortfolioImages.objects.create(influencer_username=joined_influencer, image_url=images_portfolio_url[i])
				# 	edit_port_folio.save()

				return redirect('url {influencer_profile}')
			context={'joined_influencer': joined_influencer, 'package_influencer': package_influencer, 'faq_influencer': faq_influencer}
			return render(request, 'User/infl_profile_edit.html', context)
				
			
		else:
			print("User is not logged in :(")
			# return redirect(request, 'User/influencer_profile.html')
	except Exception as e:
			messages.success(request, 'Superuser logged in')
			print(e)
	return render(request, 'User/infl_profile_edit.html')




def join_brand_profile(request):
	try:
		user= request.user
		user_email=user.email
		loggendin_brand= JoinBrand.objects.get(brand_email=user_email)
		print('_--_---------------------------------------')
		print('user_email::-------------------------------------------""::"""', loggendin_brand)
		if request.method== 'POST':
			location_brand=request.POST.get('location_brand')
			description_brand=request.POST.get('description_brand')
			brand_niches_value=request.POST.get('brand_niches_value')
			
			loggendin_brand.brand_location=location_brand
			loggendin_brand.brand_description=description_brand
			



			if "Lifestyle" in brand_niches_value:
				loggendin_brand.lifestyle= True
			if "Fashion" in brand_niches_value:
				loggendin_brand.fashion= True
			if "Beauty" in brand_niches_value:
				loggendin_brand.beauty= True
			
			if "Health & Fitness" in brand_niches_value:
				loggendin_brand.health_fitness= True
			if "Travel" in brand_niches_value:
				loggendin_brand.travel= True
			if "Food & Drink" in brand_niches_value:
				loggendin_brand.food_drink= True
			if "Model" in brand_niches_value:
				loggendin_brand.model= True
			if "Comedy & Entertainment" in brand_niches_value:
				loggendin_brand.comedy_entertainment= True
			if "Art & Photography" in brand_niches_value:
				loggendin_brand.art_photography= True
			
			if "Music & Dance" in brand_niches_value:
				loggendin_brand.music_dance= True
			if "Entrepreneur & Business" in brand_niches_value:
				loggendin_brand.entrepreneur_business= True
			if "Family & Children" in brand_niches_value:
				loggendin_brand.family_children= True
			if "Animals & Pets" in brand_niches_value:
				loggendin_brand.animals_pets= True
			if "Athlete & Sports" in brand_niches_value:
				loggendin_brand.athlete_sports= True
			if "Celebrity & Public Figure" in brand_niches_value:
				loggendin_brand.celebrity_public_pigure= True
			
			if "Adventure & Outdoors" in brand_niches_value:
				loggendin_brand.adventure_outdoors= True
			if "Actor" in brand_niches_value:
				loggendin_brand.actor= True
			if "Education" in brand_niches_value:
				loggendin_brand.education= True
			if "Gaming" in brand_niches_value:
				loggendin_brand.gaming= True
			if "LGBTQ2" in brand_niches_value:
				loggendin_brand.lgbtq= True
			if "Technology" in brand_niches_value:
				loggendin_brand.technology= True
			
			if "Healthcare" in brand_niches_value:
				loggendin_brand.healthcare= True
			if "Vegan" in brand_niches_value:
				loggendin_brand.vegan= True
			if "Cannabis" in brand_niches_value:
				loggendin_brand.cannabis= True
			if "Skilled Trades" in brand_niches_value:
				loggendin_brand.skilled_trades= True
			if "Automotive" in brand_niches_value:
				loggendin_brand.automotive= True

			profile_image= request.FILES.get('profile_img')
			print('profile image join_________________', profile_image)
			all_image= request.FILES.getlist('img-files')
			print('all_________________', all_image)
			print('length of all_________________', len(all_image))
			print('image0 allimage&&&&&&&&&&&&&', all_image[0])
			cover_image= request.FILES.get('cover_image')
			img2= request.FILES.get('img2')
			img3= request.FILES.get('img3')
			img4= request.FILES.get('img4')

			loggendin_brand.profile_image=profile_image

			if len(all_image) == 1:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				loggendin_brand.cover_image=all_image[0]
			if len(all_image) == 2:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				loggendin_brand.cover_image=all_image[0]
				loggendin_brand.image3=all_image[1]
			if len(all_image) == 3:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				loggendin_brand.cover_image=all_image[0]
				loggendin_brand.image3=all_image[1]
				loggendin_brand.image4=all_image[2]
			if len(all_image) == 4:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				loggendin_brand.cover_image=all_image[0]
				loggendin_brand.image3=all_image[1]
				loggendin_brand.image4=all_image[2]
				loggendin_brand.image5=all_image[3]

			if len(all_image) == 5:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				loggendin_brand.cover_image=all_image[0]
				loggendin_brand.image3=all_image[1]
				loggendin_brand.image4=all_image[2]
				loggendin_brand.image5=all_image[3]
			if len(all_image) == 6:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				loggendin_brand.cover_image=all_image[0]
				loggendin_brand.image3=all_image[1]
				loggendin_brand.image4=all_image[2]
				loggendin_brand.image5=all_image[3]
			if len(all_image) == 7:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				loggendin_brand.cover_image=all_image[0]
				loggendin_brand.image3=all_image[1]
				loggendin_brand.image4=all_image[2]
				loggendin_brand.image5=all_image[3]
			if len(all_image) == 8:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				loggendin_brand.cover_image=all_image[0]
				loggendin_brand.image3=all_image[1]
				loggendin_brand.image4=all_image[2]
				loggendin_brand.image5=all_image[3]
			if len(all_image) == 9:
				print('_______________________________')
				print('length of allimage&&&&&&&&&&&&&', all_image[0])
				loggendin_brand.cover_image=all_image[0]
				loggendin_brand.image3=all_image[1]
				loggendin_brand.image4=all_image[2]
				loggendin_brand.image5=all_image[3]
			if len(all_image) == 10:
				loggendin_brand.cover_image=all_image[0]
				loggendin_brand.image3=all_image[1]
				loggendin_brand.image4=all_image[2]
				loggendin_brand.image5=all_image[3]

			if cover_image:

				loggendin_brand.cover_image=cover_image
				
			if img2:
				loggendin_brand.image3=img2
			if img3:
				loggendin_brand.image4=img3
			if img4:
				loggendin_brand.image5=img4



			loggendin_brand.is_added= True
			loggendin_brand.save()
			return render(request,'User/home.html')
	except Exception as e:
			messages.success(request, 'Ooops There is a problem. Try again!!')
			print(e)
	return render(request, 'user/join_brand_profile.html')




def brand_profile(request):
	user_email = None
	try:
		if request.user.is_authenticated:
			print("brand is logged in :)")
			user= request.user
			user_email=user.email
			
			joined_brand=JoinBrand.objects.get(brand_email=user_email)
			print('joined_brand.brand_location::::::::::',joined_brand.brand_location)
			if joined_brand.brand_location is None:
				return redirect('/joinbrandprofile/')
				print('joined_influencer::::::::::',joined_brand)
			else:
				context={'joined_brand': joined_brand}
				return render(request, 'User/brand_profile.html', context)
		else:
			print("brand is not logged in :(")
			return redirect(request, 'User/influencer_profile.html')
	except Exception as e:
			messages.success(request, 'oops there was a problem')
			return redirect('home')



def brand_profile_edit(request):
	try:

		user_email= request.user.email
		user_brand=User.objects.get(email= user_email)
		
		loggendin_brand_1=JoinBrand.objects.get(brand_email=user_email)
		print('joined_brand edit', loggendin_brand_1)
		if request.method == 'POST':
			brand_location= request.POST.get('brand_location')
			print('brand_location edit', brand_location)
			brand_niches_value= request.POST.get('brand_niches_value')
			print('brand_niches_value edit', brand_niches_value)
			brand_description= request.POST.get('brand_description')
			print('brand_description edit', brand_description)
			brand_website= request.POST.get('brand_website')
			print('brand_website edit', brand_website)
			brand_instagram= request.POST.get('brand_instagram')
			print('brand_instagram edit', brand_instagram)
			brand_tiktok= request.POST.get('brand_tiktok')
			print('brand_tiktok edit', brand_tiktok)
			brand_youtube= request.POST.get('brand_youtube')
			print('brand_youtube edit', brand_youtube)
			
			
			if brand_location:
				loggendin_brand_1.brand_location=brand_location
				loggendin_brand_1.save()
			if brand_description:
				loggendin_brand_1.brand_description= brand_description
				loggendin_brand_1.save()
			if brand_website:
				loggendin_brand_1.brand_website=brand_website
				loggendin_brand_1.save()
			if brand_instagram:
				loggendin_brand_1.brand_instagram= brand_instagram
				loggendin_brand_1.save()
			if brand_tiktok:
				loggendin_brand_1.brand_tiktok=brand_tiktok
				loggendin_brand_1.save()
			if brand_youtube:
				loggendin_brand_1.brand_youtube= brand_youtube
				loggendin_brand_1.save()

			if "Lifestyle" in brand_niches_value:
				loggendin_brand_1.lifestyle= True
				loggendin_brand_1.save()
			if "Fashion" in brand_niches_value:
				loggendin_brand_1.fashion= True
				loggendin_brand_1.save()
			if "Beauty" in brand_niches_value:
				loggendin_brand_1.beauty= True
				loggendin_brand_1.save()
			
			if "Health & Fitness" in brand_niches_value:
				loggendin_brand_1.health_fitness= True
				loggendin_brand_1.save()
			if "Travel" in brand_niches_value:
				loggendin_brand_1.travel= True
				loggendin_brand_1.save()
			if "Food & Drink" in brand_niches_value:
				loggendin_brand_1.food_drink= True
				loggendin_brand_1.save()
			if "Model" in brand_niches_value:
				loggendin_brand_1.model= True
				loggendin_brand_1.save()
			if "Comedy & Entertainment" in brand_niches_value:
				loggendin_brand_1.comedy_entertainment= True
				loggendin_brand_1.save()
			if "Art & Photography" in brand_niches_value:
				loggendin_brand_1.art_photography= True
				loggendin_brand_1.save()
			
			if "Music & Dance" in brand_niches_value:
				loggendin_brand_1.music_dance= True
				loggendin_brand_1.save()
			if "Entrepreneur & Business" in brand_niches_value:
				loggendin_brand_1.entrepreneur_business= True
				loggendin_brand_1.save()
			if "Family & Children" in brand_niches_value:
				loggendin_brand_1.family_children= True
				loggendin_brand_1.save()
			if "Animals & Pets" in brand_niches_value:
				loggendin_brand_1.animals_pets= True
				loggendin_brand_1.save()
			if "Athlete & Sports" in brand_niches_value:
				loggendin_brand_1.athlete_sports= True
				loggendin_brand_1.save()
			if "Celebrity & Public Figure" in brand_niches_value:
				loggendin_brand_1.celebrity_public_pigure= True
				loggendin_brand_1.save()
			
			if "Adventure & Outdoors" in brand_niches_value:
				loggendin_brand_1.adventure_outdoors= True
				loggendin_brand_1.save()
			if "Actor" in brand_niches_value:
				loggendin_brand_1.actor= True
				loggendin_brand_1.save()
			if "Education" in brand_niches_value:
				loggendin_brand_1.education= True
				loggendin_brand_1.save()
			if "Gaming" in brand_niches_value:
				loggendin_brand_1.gaming= True
				loggendin_brand_1.save()
			if "LGBTQ2" in brand_niches_value:
				loggendin_brand_1.lgbtq= True
				loggendin_brand_1.save()
			if "Technology" in brand_niches_value:
				loggendin_brand_1.technology= True
				loggendin_brand_1.save()
			
			if "Healthcare" in brand_niches_value:
				loggendin_brand_1.healthcare= True
				loggendin_brand_1.save()
			if "Vegan" in brand_niches_value:
				loggendin_brand_1.vegan= True
				loggendin_brand_1.save()
			if "Cannabis" in brand_niches_value:
				loggendin_brand_1.cannabis= True
				loggendin_brand_1.save()
			if "Skilled Trades" in brand_niches_value:
				loggendin_brand_1.skilled_trades= True
				loggendin_brand_1.save()
			if "Automotive" in brand_niches_value:
				loggendin_brand_1.automotive= True
				loggendin_brand_1.save()




			profile_img= request.FILES.get('profile_img_edit')
			print('profile image edit_____', profile_img)
			cover_image= request.FILES.get('cover_image')
			img2= request.FILES.get('img2')
			img3= request.FILES.get('img3')
			img4= request.FILES.get('img4')

			if profile_img:
				print('^^^^^^^ Inside 1 ^^^^^^^^^^^^^^')
				loggendin_brand_1.profile_image=profile_img
				
				loggendin_brand_1.save()
			if cover_image:
				print('^^^^^^^ Inside 2 ^^^^^^^^^^^^^^')
				loggendin_brand_1.cover_image=cover_image
				
				loggendin_brand_1.save()
			if img2:
				print('^^^^^^^ Inside 3 ^^^^^^^^^^^^^^')
				loggendin_brand_1.image3=img2
				
				loggendin_brand_1.save()
			if img3:
				print('^^^^^^^ Inside 4 ^^^^^^^^^^^^^^')
				loggendin_brand_1.image4=img3
				
				loggendin_brand_1.save()
			if img4:
				print('^^^^^^^ Inside 5 ^^^^^^^^^^^^^^')
				loggendin_brand_1.image5=img4
				
				loggendin_brand_1.save()
		context={'joined_brand': loggendin_brand_1}
		return render(request, 'User/brand_edit.html', context)
	except Exception as e:
			messages.success(request, 'Ooops There is a problem. Try again!!')
			print(e)
	return render(request, 'User/brand_edit.html')








def brand_compaign(request):
	return render(request, 'User/brand_compaign.html')

def brand_order(request):
	return render(request, 'User/brand_orders.html')

def brand_pricing(request):
	return render(request, 'User/brand_pricing.html')



def influencer_home_profile(request):
	username = None

	try:

		if request.method== 'POST':
			print("User is logged in :)")
			influencer_email= request.POST.get('influencer')
			
			print("User is Home page--- :)", influencer_email)
			joined_influencer=JoinInfluencer.objects.get(email_address=influencer_email)
			username=joined_influencer.influencer_username
			print("User is Home page username--- :)", joined_influencer.influencer_username)
			package_influencer=InfluencerPackage.objects.filter(influencer_username__influencer_username=username)
			faq_influencer=InfluencerFaq.objects.filter(influencer_username__influencer_username=username)
			edit_portfolio=EditPortfolioImages.objects.filter(influencer_username__influencer_username=username)
			print('joined_influencer::::::::::',joined_influencer)
			context={'joined_influencer': joined_influencer, 'package_influencer': package_influencer, 'faq_influencer': faq_influencer, 'edit_portfolio':edit_portfolio}
			return render(request, 'User/influencer_home_profile.html', context)
		else:
			print("User is not logged in :(")

			
			return redirect(request, 'User/home.html')
	except Exception as e:
			messages.success(request, 'Oops there was a problem')
			return redirect('home')
	
def checkout(request):
	try:
		if request.method== 'POST':
			influencer_email= request.POST.get('influencer_email')
			package_category= request.POST.get('package_category')
			checkout_price= request.POST.get('checkout_price')
			checkout_price_int= checkout_price.replace('$','')
			ten_percent_price= int(checkout_price_int)/10
			total_price= int(checkout_price_int)+ ten_percent_price
			print('checkout_price:::::::::::::::::::',checkout_price_int)
			print('influencer_email:::::::::::::::::::',influencer_email)
			print('tenpercent:::::::::::::::::::',ten_percent_price)
			print('total:::::::::::::::::::',total_price)
			joined_influencer=JoinInfluencer.objects.get(email_address=influencer_email)
			context= {'joined_influencer': joined_influencer , 'package_category':package_category, 'checkout_price':checkout_price_int, 'ten_percent_price':ten_percent_price,'total_price': total_price}
			return render(request, 'User/checkout.html', context)
		else:
			return redirect(request, 'User/home.html')
	except Exception as e:
			messages.success(request, 'Oops There is some problem. Place order again')
			return redirect('home')

def custom_offer(request):
	if request.method== 'POST':
		influencer_email= request.POST.get('influencer_email_custom')
		context={'influencer_email': influencer_email}
	return render(request, 'User/custom_offer.html', context)


def create_checkout_session(request):
	try:
		if request.method== 'POST':
			total_checkout_price=request.POST.get('total_checkout_price')
			package_category=request.POST.get('package_category')
			total= total_checkout_price.split('.')
			print('total_checkout_price@@@@@@@', total_checkout_price)
			checkout_session=stripe.checkout.Session.create(
				payment_method_types= ['card'],
				line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': package_category,
        },
        'unit_amount': int(total[0])*100,
      },
      'quantity': 1,
    }],
				# line_items=[
				# # {
				# # 	# Provide the exact Price ID (for example, pr_1234) of the product you want to sell
				# # 	'price': 'price_1Ksvf3GppnrRkU6FcbHEkX4r',
				# # 	'quantity': 1,
				# # },
				
				# ],

				mode='payment',
				
				success_url='http://164.90.199.198:8000' + '/success',
				cancel_url='http://164.90.199.198:8000' + '/cancel',
				# success_url='http://127.0.0.1:8000' + '/success',
				# cancel_url='http://127.0.0.1:8000' + '/cancel',
			)
			return redirect(checkout_session.url)
	except Exception as e:
		print(e)
		messages.success(request, 'Oops There is some problem. Place order again')
		return redirect('checkout_page')
		

def success_view(request):
    return render(request, 'User/success.html')

def cancel_view(request):
    return render(request, 'User/cancel.html')



def social_signup(request):
	return render(request,'User/social_signup.html')

def categories(request):
	try:
		user_email_inful=request.user.email
		session_user=request.session.get('username_session')
		print('user_email_inful::::::@@@@',user_email_inful)
		if JoinInfluencer.objects.filter(email_address= user_email_inful):
			return redirect('/joininfluencerprofilepage')
		if session_user is not None:
			print('------------------------Session User', session_user)

			join_inful=JoinInfluencer.objects.filter(influencer_username= session_user)
			if join_inful:
				print('------------------------join_inful', join_inful)
				join_inful_0=join_inful[0]
				if join_inful_0.email_address != '':
					print('------------------------join_inful.email_address', join_inful_0.email_address)
					if join_inful_0.email_address == user_email_inful:
						print('------------------------Inside equal if')
						return redirect('/joininfluencerprofilepage')
					else:
						print('------------------------Inside equal else')
						messages.success(request, 'Email You trying to login does not exist')
						return redirect('logout')
				else:
					print('------------------------join_inful.email_address Else', join_inful_0.email_address)
					if request.method== 'POST':
						try:
							if request.user.is_authenticated:
								print("brand is logged in :)")
								user= request.user
								username = request.user.username
								user_email=user.email
								fname_influencer=request.user.first_name
								lname_influencer=request.user.last_name
								fullname_influencer= fname_influencer+' '+ lname_influencer
								print('username::::::@@@@',username)
								print('user_email::::::@@@@',user_email)
								print('fname_influencer::::::@@@@',fname_influencer)
								print('Flname_influencer::::::@@@@',lname_influencer)
								print('fullname_influencer::::::@@@@',fullname_influencer)
								username_session = request.session.get('username_session')
								print('Fav username_session create page::::::@@@@',username_session)
								influencer=User.objects.get(username= username)
								influencer_obj= JoinInfluencer.objects.get(influencer_username= username_session)
								influencer_obj.full_name=fullname_influencer
								influencer_obj.email_address=user_email
								niches= request.POST.get('niches_val')
								if "Lifestyle" in niches:
									influencer_obj.lifestyle= True
								if "Fashion" in niches:
									influencer_obj.fashion= True
								if "Beauty" in niches:
									influencer_obj.beauty= True
								
								if "Health & Fitness" in niches:
									influencer_obj.health_fitness= True
								if "Travel" in niches:
									influencer_obj.travel= True
								if "Food & Drink" in niches:
									influencer_obj.food_drink= True
								if "Model" in niches:
									influencer_obj.model= True
								if "Comedy & Entertainment" in niches:
									influencer_obj.comedy_entertainment= True
								if "Art & Photography" in niches:
									influencer_obj.art_photography= True
								
								if "Music & Dance" in niches:
									influencer_obj.music_dance= True
								if "Entrepreneur & Business" in niches:
									influencer_obj.entrepreneur_business= True
								if "Family & Children" in niches:
									influencer_obj.family_children= True
								if "Animals & Pets" in niches:
									influencer_obj.animals_pets= True
								if "Athlete & Sports" in niches:
									influencer_obj.athlete_sports= True
								if "Celebrity & Public Figure" in niches:
									influencer_obj.celebrity_public_pigure= True
								
								if "Adventure & Outdoors" in niches:
									influencer_obj.adventure_outdoors= True
								if "Actor" in niches:
									influencer_obj.actor= True
								if "Education" in niches:
									influencer_obj.education= True
								if "Gaming" in niches:
									influencer_obj.gaming= True
								if "LGBTQ2" in niches:
									influencer_obj.lgbtq= True
								if "Technology" in niches:
									influencer_obj.technology= True
								
								if "Healthcare" in niches:
									influencer_obj.healthcare= True
								if "Vegan" in niches:
									influencer_obj.vegan= True
								if "Cannabis" in niches:
									influencer_obj.cannabis= True
								if "Skilled Trades" in niches:
									influencer_obj.skilled_trades= True
								if "Automotive" in niches:
									influencer_obj.automotive= True
								niches_updated = niches.rstrip(',')
								influencer_obj.description_influencer=niches
							
								influencer_obj.save()
								is_brand_obj= BrandorInfluencer.objects.create(user=influencer, brand=False)
								is_brand_obj.save()
								return render(request,'User/join_influencer_profile.html')
						except Exception as e:
							print(e)
			
		else:
			print('------------------------Session User Else')
			messages.success(request, 'Email You trying to login does not exist')
			return redirect('logout')
	except Exception as e:
			messages.success(request, 'Ooops There is a problem. Try again!!')
			print(e)
	return render(request,'User/categories.html')

def join_influencer_profile_page(request):
	user_email_inful=request.user.email
	print('user_email_inful::::::@@@@',user_email_inful)
	inful=JoinInfluencer.objects.get(email_address= user_email_inful)
	if inful.location:
		return redirect('/')
	return render(request,'User/join_influencer_profile.html')


def delete_profile_pic(request):
	user_email_inful=request.user.email
	# if request.method == 'POST':
	# profile_pic= request.POST.get('profile_img_edit_2')
	inful=JoinInfluencer.objects.get(email_address= user_email_inful)
	inful_profile_pic= inful.profile_image
	inful_profile_pic.delete()
	return redirect('/influencerprofile')