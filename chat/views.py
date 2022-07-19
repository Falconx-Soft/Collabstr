from django.shortcuts import render, redirect
from django.conf import settings
from user.models import *
from chat.models import PrivateChatRoom, RoomChatMessage
import json
from django.http import HttpResponse
from user.models import *

DEBUG = False

def private_chat_room_view(request, *args, **kwargs):
	user = request.user

	# Redirect them if not authenticated
	if not user.is_authenticated:
		return redirect("login")

	# context = {}
	# context['debug'] = DEBUG
	# context['debug_mode'] = settings.DEBUG

	if request.method== 'POST':
		status = request.POST.get('display_order_status')
		id = request.POST.get('display_order_id')
		order_T = Orders.objects.get(id=id)
		order_T.status = status
		order_T.save()
	if request.user.is_brand:
		joinBrandObj = JoinBrand.objects.get(user=request.user)
		order_obj = Orders.objects.filter(brand=joinBrandObj)

		context = {
			'debug':DEBUG,
			'debug_mode':settings.DEBUG,
			'pending_orders':order_obj,
			'display_order':order_obj[0]
		}
		return render(request, 'chat/order.html',context)
	else:
		influencer_obj = JoinInfluencer.objects.get(user=request.user)
		order_obj = Orders.objects.filter(influencer=influencer_obj)

		if order_obj:

			context = {
				'debug':DEBUG,
				'debug_mode':settings.DEBUG,
				'pending_orders':order_obj,
				'display_order':order_obj[0]
			}
		else:
			context = {
				'debug':DEBUG,
				'debug_mode':settings.DEBUG,
				'pending_orders':order_obj,
				'display_order':''
			}
		return render(request, 'chat/order.html',context)

# Ajax call to return a private chatroom or create one if does not exist
def create_or_return_private_chat(request, *args, **kwargs):
	user1 = request.user
	payload = {}
	if user1.is_authenticated:
		if request.method == "POST":
			order_id = request.POST.get("order_id")
			print(order_id,"********id**********")
			order = Orders.objects.get(id=order_id)
			try:
				chat = PrivateChatRoom.objects.get(order=order)
				payload['response'] = "Successfully got the chat."
				payload['chatroom_id'] = chat.id

				# payload['choose_platform'] = order.package.choose_platform
				# payload['content_category'] = order.package.content_category
				# payload['package_offering'] = order.package.package_offering
				# payload['package_include'] = order.package.package_include
				# payload['package_price'] = order.package.package_price

				payload['status'] = order.status

			except JoinInfluencer.DoesNotExist:
				payload['response'] = "Unable to start a chat with that user."
	else:
		payload['response'] = "You can't start a chat if you are not authenticated."
	return HttpResponse(json.dumps(payload), content_type="application/json")
