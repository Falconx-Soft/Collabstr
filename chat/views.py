from django.shortcuts import render, redirect
from django.conf import settings
from user.models import JoinInfluencer, JoinInfluencer
from chat.models import PrivateChatRoom, RoomChatMessage
import json
from django.http import HttpResponse
from user.models import *
from .utils import find_or_create_private_chat
from django.contrib.auth import get_user_model
from django.core import serializers
from datetime import timedelta
from django.db.models.functions import Now
import stripe
User = get_user_model()


DEBUG = False

def private_chat_room_view(request, *args, **kwargs):
	user = request.user

	# Redirect them if not authenticated
	if not user.is_authenticated:
		return redirect("login")

	if request.user.is_brand:
		brand_obj = JoinBrand.objects.get(user=request.user)
		chat_room = PrivateChatRoom.objects.filter(brand=brand_obj)

		if chat_room:

			context = {
				'debug':DEBUG,
				'debug_mode':settings.DEBUG,
				'chat_room':chat_room,
				'chat_room_display':chat_room[0],
				'friend_id': chat_room[0].influencer.user.id
			}
		else:
			context = {
				'debug':DEBUG,
				'debug_mode':settings.DEBUG,
				'chat_room':chat_room,
				'chat_room_display':''
			}
		return render(request, 'chat/order.html',context)
	else:
		influencer_obj = JoinInfluencer.objects.get(user=request.user)
		chat_room = PrivateChatRoom.objects.filter(influencer=influencer_obj)

		if chat_room:

			context = {
				'debug':DEBUG,
				'debug_mode':settings.DEBUG,
				'chat_room':chat_room,
				'chat_room_display':chat_room[0],
				'friend_id': chat_room[0].brand.user.id
			}
		else:
			context = {
				'debug':DEBUG,
				'debug_mode':settings.DEBUG,
				'chat_room':chat_room,
				'chat_room_display':''
			}
		return render(request, 'chat/order.html',context)

def get_order_list(orders_obj):

	order_list = []

	for order in orders_obj:
		temp = {
			'influencer_name':order.influencer.full_name,
			'brand_name':order.brand.full_name,
			'date':str(order.timestamp.date()),
			'price':order.price,
			'status':order.status
		}
		order_list.append(temp)

	return order_list

# Ajax call to return a private chatroom or create one if does not exist
def create_or_return_private_chat(request, *args, **kwargs):
	user1 = request.user
	payload = {}
	if user1.is_authenticated:
		if request.method == "POST":
			user2_id = request.POST.get("user2_id")
			try:
				user2 = User.objects.get(id=user2_id)
				if request.user.is_brand:
					brand_obj = JoinBrand.objects.get(user=user1)
					influencer_obj = JoinInfluencer.objects.get(user=user2)
					chat = PrivateChatRoom.objects.get(brand=brand_obj, influencer=influencer_obj)

					temp_orders = Orders.objects.filter(timestamp__lte=Now()-timedelta(days=3))

					for odr in temp_orders:
						odr.delete()

					orders_obj = Orders.objects.filter(influencer=influencer_obj, brand=brand_obj, status="pending")
					panding_orders = get_order_list(orders_obj)

					orders_obj = Orders.objects.filter(influencer=influencer_obj, brand=brand_obj, status="accept")
					accept_orders = get_order_list(orders_obj)

					orders_obj = Orders.objects.filter(influencer=influencer_obj, brand=brand_obj, status="complete")
					complete_orders = get_order_list(orders_obj)

					payload['response'] = "Successfully got the chat."
					payload['chatroom_id'] = chat.id
					payload['panding_orders'] = panding_orders
					payload['accept_orders'] = accept_orders
					payload['complete_orders'] = complete_orders
				else:
					brand_obj = JoinBrand.objects.get(user=user2)
					influencer_obj = JoinInfluencer.objects.get(user=user1)
					chat = PrivateChatRoom.objects.get(brand=brand_obj, influencer=influencer_obj)
					
					orders_obj = Orders.objects.filter(influencer=influencer_obj, brand=brand_obj, status="pending")
					panding_orders = get_order_list(orders_obj)

					orders_obj = Orders.objects.filter(influencer=influencer_obj, brand=brand_obj, status="accept")
					accept_orders = get_order_list(orders_obj)

					orders_obj = Orders.objects.filter(influencer=influencer_obj, brand=brand_obj, status="complete")
					complete_orders = get_order_list(orders_obj)

					payload['response'] = "Successfully got the chat."
					payload['chatroom_id'] = chat.id
					payload['panding_orders'] = panding_orders
					payload['accept_orders'] = accept_orders
					payload['complete_orders'] = complete_orders
			except User.DoesNotExist:
				payload['response'] = "Unable to start a chat with that user."
	else:
		payload['response'] = "You can't start a chat if you are not authenticated."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def start_new_chat(request,id):
	brand_obj = JoinBrand.objects.get(user=request.user)
	chat_room = PrivateChatRoom.objects.filter(brand=brand_obj)
	influencer_obj = JoinInfluencer.objects.get(id=id)

	if chat_room:

		context = {
			'debug':DEBUG,
			'debug_mode':settings.DEBUG,
			'chat_room':chat_room,
			'chat_room_display':chat_room[0],
			'friend_id': influencer_obj.user.id
		}
	else:
		context = {
			'debug':DEBUG,
			'debug_mode':settings.DEBUG,
			'chat_room':chat_room,
			'chat_room_display':''
		}
	return render(request, 'chat/order.html',context)

