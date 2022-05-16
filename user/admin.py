from django.contrib import admin
from .models import*
# Register your models here.

admin.site.register(accountsCheck)
# admin.site.register(JoinInfluencer)
admin.site.register(InfluencerPackage)
admin.site.register(InfluencerFaq)
admin.site.register(EditPortfolioImages)
admin.site.register(BrandorInfluencer)
admin.site.register(JoinBrand)
# admin.site.register(User)

admin.site.register(submit_requirements)
admin.site.register(Orders)


class InfluencerAdmin(admin.ModelAdmin):
    list_display = ('influencer_username', 'full_name', 'email_address')
admin.site.register(JoinInfluencer, InfluencerAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name')
admin.site.register(User, UserAdmin)