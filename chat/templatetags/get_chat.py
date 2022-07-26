from atexit import register
from django import template
from requests import request
from chat.models import RoomChatMessage,PrivateChatRoom
from user.models import Orders
register= template.Library()
@register.filter(name='get_chat')
def get_chat(id,request):
    chat = PrivateChatRoom.objects.get(id=id)
    try:
        PreviousChat_obj = RoomChatMessage.objects.filter(room=chat).order_by('-id')[0]
        return PreviousChat_obj.content[:30]
    except:
        return ""