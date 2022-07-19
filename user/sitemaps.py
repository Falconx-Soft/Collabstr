from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import JoinBrand

class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return[
            'home',
            'after_brand_signup',
            'login',
            'register',
            'logout',
            'join_as_brand',
            'join_as_influencer',
            'create_your_page',
            'join_influencer_profile',
            'influencer_profile',
            'influencer_profile_edit',
            'influencer_home_profile',
            'checkout_page',
            'custom_offer',
            'join_brand_profile',
            'brand_profile',
            'brand_profile_edit',
            'brand_compaign',
            'brand_order',
            'brand_pricing',
            'checkout',
            'success',
            'cancel',
            'social_signup',
            'join_influencer_profile_page',
            'categories',
            'delete_profile_pic',
            'reset_password',
            'checkout_requirements',
            'placeOrder',
            'order',
            'dashboard',
            'get_images',
            'privacy',
            'terms',
            'faq',
            'sitemap',
            'contact_us',
            ]

    def location(self, item):
        return reverse(item)