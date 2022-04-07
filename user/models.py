from distutils.command.upload import upload
from email.mime import image
from operator import truediv
from pickle import TRUE
from pyexpat import model
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class accountsCheck(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    crated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class JoinInfluencer(models.Model):
    influencer_username= models.CharField(max_length=50)
    full_name= models.CharField(max_length=150,default="")
    email_address= models.EmailField(max_length=300, default="")
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

   

     




    def __str__(self):
            return self.influencer_username


class InfluencerPackage(models.Model):
    influencer_username= models.ForeignKey(JoinInfluencer,on_delete=models.CASCADE)
    choose_platform=models.CharField(max_length=100, default="")
    content_category= models.CharField(max_length=50, default="")
    package_offering=models.CharField(max_length=500, default="")
    package_include=models.CharField(max_length=1000, default="")
    package_price=models.IntegerField(default=0)
    
    
    
    def __str__(self):
            return self.influencer_username.influencer_username

class InfluencerFaq(models.Model):
    influencer_username=models.ForeignKey(JoinInfluencer, on_delete=models.CASCADE)
    faq_question=models.CharField(max_length=500)
    faq_answer=models.CharField(max_length=700)



    def __str__(self):
            return self.influencer_username.influencer_username
