from django.contrib import admin
from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
      path('', views.home, name="home"),
      path('afterbrandsignup/', views.ater_brand_signup, name="after_brand_signup"),
    path('login/', views.loginUser, name="login"),
	path('register/', views.register, name="register"),
      
	path('logout/', views.logoutUser, name="logout"),

	
      path('joinasbrand/', views.join_as_brand, name="join_as_brand"),
      path('joinasinfluencer/', views.join_as_influencer, name="join_as_influencer"),
      path('createyourpage/', views.create_your_page, name="create_your_page"),
      path('joininfluencerprofile/', views.join_influencer_profile, name="join_influencer_profile"),
      path('influencerprofile/', views.influencer_profile, name="influencer_profile"),
      path('influenceredit/', views.influencer_profile_edit, name="influencer_profile_edit"),



      path('influencerhomeprofile/', views.influencer_home_profile, name="influencer_home_profile"),
      path('checkout/', views.checkout, name="checkout_page"),
      path('customoffer/', views.custom_offer, name="custom_offer"),




      path('joinbrandprofile/', views.join_brand_profile, name="join_brand_profile"),  
      path('brandprofile/', views.brand_profile, name="brand_profile"),   
      path('brandedit/', views.brand_profile_edit, name="brand_profile_edit"),
      path('brandcompaign/', views.brand_compaign, name="brand_compaign"),
      path('brandorder/', views.brand_order, name="brand_order"),
      path('brandpricing/', views.brand_pricing, name="brand_pricing"),


      path('create-checkout-session/', views.create_checkout_session, name="checkout"),
      path('success/',views.success_view, name="success"),
      path('cancel/',views.cancel_view, name="cancel"),

      path('socialsignup/',views.social_signup, name="social_signup"),
      path('joininfluencerprofilepage/',views.join_influencer_profile_page, name="join_influencer_profile_page"),
      path('categories/',views.categories, name="categories"),



      path('deleteprofilepic/',views.delete_profile_pic, name="delete_profile_pic"),
      

	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="User/restPassword/restPassword.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="User/restPassword/passwordRestSend.html"),
          name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="User/restPassword/newPssword.html"),
          name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="User/restPassword/passwordResetComplete.html"),
          name="password_reset_complete"),

      path('checkout_requirements/', views.checkout_requirements, name="checkout_requirements"),

      path('placeOrder/', views.placeOrder, name="placeOrder"),

      path('order/', views.order, name="order"),

      path('order/<int:id>/', views.order_by_id, name="order_by_id"),

      path('dashboard/', views.dashboard, name="dashboard"),

      path('get_images/', views.get_images, name="get_images"),
]
