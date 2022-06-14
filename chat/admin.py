from django.contrib import admin
from .models import*
# Register your models here.

class ChatMessage(admin.ModelAdmin):
    readonly_fields = ('user','room','timestamp','content')

admin.site.register(PrivateChatRoom)
admin.site.register(RoomChatMessage,ChatMessage)