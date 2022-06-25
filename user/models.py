from distutils.command.upload import upload
import email
from email.mime import image
from hashlib import blake2s
from operator import truediv
from pickle import TRUE
from pyexpat import model
from re import T
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from requests import request

# Create your models here.
class User(AbstractUser):
    is_brand = models.BooleanField(default=False, null= True, blank=True)

class accountsCheck(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    crated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
class BrandorInfluencer(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    brand= models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class JoinInfluencer(models.Model):
    influencer_username= models.CharField(max_length=200)
    full_name= models.CharField(max_length=150,default="")
    email_address= models.EmailField(max_length=300, default="")
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    password= models.CharField(max_length=30,default="")
    location= models.CharField(max_length=100, default="")
    title_influencer= models.CharField(max_length=80,default="")
    description_influencer=models.CharField(max_length=1000, default="")
    gender_influencer=models.CharField(max_length=20, default="")
    instagram_username=models.CharField(max_length=100,default="",null=True,blank=True)
    instagram_followers=models.CharField(max_length=20, default="",null=True,blank=True)
    tiktok_username=models.CharField(max_length=100,default="",null=True,blank=True)
    tiktok_followers=models.CharField(max_length=10,default="",null=True,blank=True)
    youtube_url= models.URLField(max_length=200, default="",null=True,blank=True)
    youtube_followers=models.CharField(max_length=10,default="",null=True, blank=True)
    twitter_username=models.CharField(max_length=200,default="",null=True,blank=True)
    twitter_followers= models.CharField(max_length=10, default="",null=True, blank=True)
    twitch_username=models.CharField(max_length=200, default="",null=True, blank=True)
    twitch_followers=models.CharField(max_length=20, default="",null=True, blank=True)
    website= models.URLField(max_length=200,default="",null=True, blank=True)
   
    lifestyle=models.BooleanField(default=False)
    fashion=models.BooleanField(default=False)
    beauty=models.BooleanField(default=False)            
    health_fitness=models.BooleanField(default=False)
    travel=models.BooleanField(default=False)
    food_drink=models.BooleanField(default=False)
    model=models.BooleanField(default=False)
    comedy_entertainment=models.BooleanField(default=False)
    art_photography=models.BooleanField(default=False)
    music_dance=models.BooleanField(default=False)
    entrepreneur_business=models.BooleanField(default=False)
    family_children=models.BooleanField(default=False)
    animals_pets=models.BooleanField(default=False)
    athlete_sports=models.BooleanField(default=False)
    celebrity_public_pigure=models.BooleanField(default=False)
    adventure_outdoors=models.BooleanField(default=False)
    actor=models.BooleanField(default=False)
    education=models.BooleanField(default=False)
    gaming=models.BooleanField(default=False)
    lgbtq=models.BooleanField(default=False)
    technology=models.BooleanField(default=False)
    healthcare=models.BooleanField(default=False)
    vegan=models.BooleanField(default=False)
    cannabis=models.BooleanField(default=False)
    skilled_trades=models.BooleanField(default=False)
    automotive=models.BooleanField(default=False)
    
    
    profile_image=models.ImageField(null=True, blank=True, upload_to="images/")
    cover_image=models.ImageField(null=True, blank=True,upload_to="images/")
    image3= models.ImageField(null=True, blank=True,upload_to="images/")
    image4=models.ImageField(null=True,blank=True,upload_to="images/")
    image5=models.ImageField(null=True, blank=True,upload_to="images/")
    crated_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
            return self.influencer_username


class PreviousExprience(models.Model):
    influencer = models.ForeignKey(JoinInfluencer,on_delete=models.CASCADE)
    exprience_title = models.CharField(max_length=1000, default="", null=True, blank=True)

    def __str__(self):
          return self.exprience_title


class PreviousExprienceImages(models.Model):
    influencer = models.ForeignKey(PreviousExprience,on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True,upload_to="images/")

    def __str__(self):
          return self.influencer.influencer.user.username


class InfluencerPackage(models.Model):
    influencer_username= models.ForeignKey(JoinInfluencer,on_delete=models.CASCADE)
    choose_platform=models.CharField(max_length=100, default="",null=True, blank=True)
    content_category= models.CharField(max_length=50, default="",null=True, blank=True)
    package_offering=models.CharField(max_length=500, default="",null=True, blank=True)
    package_include=models.CharField(max_length=1000, default="", null=True, blank=True)
    package_price=models.IntegerField(default=0, null=True, blank=True)
    
    
    
    def __str__(self):
          return self.influencer_username.influencer_username


class InfluencerFaq(models.Model):
    influencer_username=models.ForeignKey(JoinInfluencer, on_delete=models.CASCADE)
    faq_question=models.CharField(max_length=500)
    faq_answer=models.CharField(max_length=700)



    def __str__(self):
            return self.influencer_username.influencer_username



class EditPortfolioImages(models.Model):
    influencer_username=models.ForeignKey(JoinInfluencer, on_delete=models.CASCADE)
    image_url= models.ImageField(max_length=300, default="", null=True, blank=True)
   
   
   
   
    def __str__(self):
            return self.influencer_username.influencer_username



class JoinBrand(models.Model):
    full_name= models.CharField(max_length=50)
    brand_name=models.CharField(max_length=50)
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    brand_website=models.URLField(max_length=300, null=True, blank=True)
    brand_instagram= models.CharField(max_length=50, blank=True, null=True)
    brand_tiktok=models.CharField(max_length=50, blank=True, null=True)
    brand_youtube= models.URLField(max_length=300, null=True, blank=True)
    brand_location= models.CharField(max_length=100, null=True, blank=True)
    brand_description= models.CharField(max_length=400, null=True, blank=True)
    
    lifestyle=models.BooleanField(default=False)
    fashion=models.BooleanField(default=False)
    beauty=models.BooleanField(default=False)            
    health_fitness=models.BooleanField(default=False)
    travel=models.BooleanField(default=False)
    food_drink=models.BooleanField(default=False)
    model=models.BooleanField(default=False)
    comedy_entertainment=models.BooleanField(default=False)
    art_photography=models.BooleanField(default=False)
    music_dance=models.BooleanField(default=False)
    entrepreneur_business=models.BooleanField(default=False)
    family_children=models.BooleanField(default=False)
    animals_pets=models.BooleanField(default=False)
    athlete_sports=models.BooleanField(default=False)
    celebrity_public_pigure=models.BooleanField(default=False)
    adventure_outdoors=models.BooleanField(default=False)
    actor=models.BooleanField(default=False)
    education=models.BooleanField(default=False)
    gaming=models.BooleanField(default=False)
    lgbtq=models.BooleanField(default=False)
    technology=models.BooleanField(default=False)
    healthcare=models.BooleanField(default=False)
    vegan=models.BooleanField(default=False)
    cannabis=models.BooleanField(default=False)
    skilled_trades=models.BooleanField(default=False)
    automotive=models.BooleanField(default=False)


    profile_image=models.ImageField(null=True, blank=True, upload_to="images/")
    cover_image=models.ImageField(null=True, blank=True,upload_to="images/")
    image3= models.ImageField(null=True, blank=True,upload_to="images/")
    image4=models.ImageField(null=True,blank=True,upload_to="images/")
    image5=models.ImageField(null=True, blank=True,upload_to="images/")
    crated_at = models.DateField(auto_now_add=True, null=True)


    is_added= models.BooleanField(default=False)

    def __str__(self):
            return self.full_name

class Orders(models.Model):
    influencer = models.ForeignKey(JoinInfluencer,on_delete=models.CASCADE)
    package = models.ForeignKey(InfluencerPackage,on_delete=models.CASCADE)
    brand = models.ForeignKey(JoinBrand,on_delete=models.CASCADE)
    status = models.CharField(max_length=500, null=True)
    crated_at = models.DateField(auto_now_add=True, null=True)

class submit_requirements(models.Model):
    description = models.CharField(max_length=2000)
    requiremerts = models.CharField(max_length=2000)
    need = models.CharField(max_length=2000)
    apply = models.CharField(max_length=500)
    additional_info = models.CharField(max_length=2000)
    re_use = models.BooleanField()
    name_of_answer = models.CharField(max_length=500)
    influencer = models.ForeignKey(JoinInfluencer, on_delete=models.CASCADE)
    orders = models.OneToOneField(Orders, on_delete=models.CASCADE, null=True)

