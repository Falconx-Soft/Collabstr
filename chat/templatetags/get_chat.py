from atexit import register
from django import template
from requests import request
from chat.models import RoomChatMessage,PrivateChatRoom
from user.models import Orders
register= template.Library()
@register.filter(name='get_chat')
def get_chat(id,request):
    orders_obj = Orders.objects.get(id=id)
    chat = PrivateChatRoom.objects.get(order=orders_obj)

    try:
        PreviousChat_obj = RoomChatMessage.objects.filter(room=chat).order_by('-id')[0]
        return PreviousChat_obj.content[:30]
    except:
        return ""