from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
import os

# LINEbot Moudle
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

# models
from user_server_1.models import *

import random

p_bot_api = LineBotApi(settings.LINE_CHANNEL_DATA['USER']['ACCESS_TOKEN'])
parser = WebhookParser(settings.LINE_CHANNEL_DATA['USER']['SECRET'])

# Create your views here.
@csrf_exempt
def index(request):
    return render(request, 'index.html', locals())


@csrf_exempt
def test(request):
    return render(request, 'test.html', locals())

@csrf_exempt
def card(request):
    img_list = [
                "https://images.unsplash.com/photo-1479660656269-197ebb83b540?dpr=2&auto=compress,format&fit=crop&w=1199&h=798&q=80&cs=tinysrgb&crop=",
                "https://images.unsplash.com/photo-1479659929431-4342107adfc1?dpr=2&auto=compress,format&fit=crop&w=1199&h=799&q=80&cs=tinysrgb&crop=",
                "https://images.unsplash.com/photo-1479644025832-60dabb8be2a1?dpr=2&auto=compress,format&fit=crop&w=1199&h=799&q=80&cs=tinysrgb&crop=",
                "https://images.unsplash.com/photo-1479621051492-5a6f9bd9e51a?dpr=2&auto=compress,format&fit=crop&w=1199&h=811&q=80&cs=tinysrgb&crop="
            ]
    
    if request.method == 'POST':
        if request.POST['status'] == 'Update':
            n = int(request.POST['count'])
            print(n)
            
            cards = list(Card.objects.all().values())[n:]       
            imgs = [img_list[random.randint(0,3)] for i in range(len(cards))]
            print(str(len(cards)) + " " + str(len(imgs)))
            content = list(zip(imgs, cards))
            new = len(imgs) > 0
            return JsonResponse({"content" : content, 'new':new})
    
    else:
        cards = Card.objects.all()
    
        imgs = [img_list[i] for i in random.sample(range(0,3), len(cards))]
        print(str(len(cards)) + " " + str(len(imgs)))
        content = list(zip(imgs, cards))

    return render(request, 'card.html', locals())
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            uid = event.source.user_id  # ID訊息
            print(f"帳號: {uid}\n訊息: {event.message.text}")
            try:
                if isinstance(event, MessageEvent):  #訊息事件
                    
                    if event.message.text in ["早安"]: #使用說明書
                        message = TextSendMessage(text=f"""早安唷""")
                    else:
                        message = TextSendMessage(text=f"""嗨嗨""")
                p_bot_api.reply_message(event.reply_token, message)  # time.sleep(10)
            except:
                break
        return HttpResponse()
    else:
        return HttpResponseBadRequest()