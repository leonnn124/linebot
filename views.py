from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot.models.events import FollowEvent
import numpy as np
import string
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction,
    CarouselTemplate,
    CarouselColumn,
    URITemplateAction,
    LocationMessage,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    ConfirmTemplate,
    QuickReply,
    QuickReplyButton,
    MessageAction
)
from linebot.models.events import FollowEvent

from . import Insurance,judge,type,conpare

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


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
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                
                if Insurance.judge == "true" :
                    Insurance.judge = ""
                    Insurance.keyword = Insurance.keyword + "&智齒"
                    result = Insurance.run()
                    arr_res=np.array(result)
                    url=Insurance.Select_Url(event.message.text)
                    arr_url=np.array(url)
                    Insurance.x=arr_url[0][0]
                    Insurance.y=arr_url[0][1]
                    Insurance.a=arr_res[0]
                    Insurance.b=arr_res[1]
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Carousel template',
                            template=CarouselTemplate(
                                columns=[
                                    CarouselColumn(
                                        thumbnail_image_url="https://imgur.com/jvef9ek.jpg",
                                        title="關鍵字 : " + Insurance.keyword,
                                        text=Insurance.a[0:60],
                                        actions=[
                                            PostbackTemplateAction(
                                                label='看更多',
                                                text='看更多',
                                                data='1A&看更多'
                                            ),
                                            PostbackTemplateAction(
                                                label='PDF',
                                                text='PDF',
                                                data='1B&PDF'
                                            ),
                                            PostbackTemplateAction(
                                                label='搜尋法條及解釋',
                                                text='搜尋法條及解釋',
                                                data='1C&搜尋法條及解釋'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url="https://imgur.com/jvef9ek.jpg",
                                        title="關鍵字 : " + Insurance.keyword,
                                        text=Insurance.b[0:60],
                                        actions=[
                                            PostbackTemplateAction( 
                                                label='看更多',
                                                text='看更多',
                                                data='2A&看更多'
                                            ),
                                            PostbackTemplateAction(
                                                label='PDF',
                                                text='PDF',
                                                data='2B&PDF'
                                            ),
                                            PostbackTemplateAction(
                                                label='搜尋法條及解釋',
                                                text='搜尋法條及解釋',
                                                data='2C&搜尋法條及解釋'
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                )

                if event.message.text == "開始查詢🔍":  
                    #Insurance.judge = "true"
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text="請輸入關鍵字⌨️")
                )

                if event.message.text == "複雜齒切除":  
                    Insurance.keyword = event.message.text
                    Insurance.judge = "true"
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Carousel template',
                            template=
                            ConfirmTemplate(
                                title='title',
                                text='" ' + event.message.text + ' " 通常與 智齒 一起搜尋 ,\n是否將 智齒 一併加入關鍵字中 ?',
                                actions=[                              
                                    PostbackTemplateAction(
                                        label='不用了',
                                        text='不用了',
                                        data='N&不用了'
                                    ),
                                    PostbackTemplateAction(
                                        label='好',
                                        text='好',
                                        data='Y&好'
                                    )
                                ]
                            )     
                        )
                )

                if event.message.text == "進階查詢":
                    type.ty=""
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text="請選擇查詢類別",
                            quick_reply=QuickReply(
                                items=[
                                    QuickReplyButton(
                                        action=MessageAction(label="關鍵字查詢",text="關鍵字查詢")
                                    ),
                                    QuickReplyButton(
                                        action=MessageAction(label="時間查詢",text="時間查詢")
                                    ),
                                    QuickReplyButton(
                                        action=MessageAction(label="委員查詢",text="委員查詢")
                                    ),
                                    QuickReplyButton(
                                        action=MessageAction(label="法條查詢",text="法條查詢")
                                    )
                                ]
                            )
                        )
                )
                
                if type.ty != "":
                    res=type.type(event.message.text)
                    #res=conpare(type.ty,type.conpare)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=res)
                )


                if event.message.text == "關鍵字查詢":
                    judge.mode(event.message.text)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入關鍵字")
                )

                if event.message.text == "時間查詢":
                    judge.mode(event.message.text)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入日期 西元/民國 皆可\n(系統將以最近的日期優先顯示)")
                )

                if event.message.text == "委員查詢":
                    judge.mode(event.message.text)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入委員姓名")
                )

                if event.message.text == "法條查詢":
                    judge.mode(event.message.text)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入法條")
                )

                

            elif isinstance(event, PostbackEvent): 

                if event.postback.data[0:3] == "law": 
                    line_bot_api.reply_message(  
                            event.reply_token,
                            TextSendMessage(text="保險法第54條第2項規定，保險契約之解釋，應探求契約當事人之真意，不得拘泥於所用之文字；如有疑義時，以作有利於被保險人之解釋為原則。")
                        )

                if event.postback.data[0:1] == "1": 

                    if event.postback.data[1:2] == "A": 
                        line_bot_api.reply_message(  
                            event.reply_token,
                            TextSendMessage(text=Insurance.a)
                        )
                    if event.postback.data[1:2] == "B": 
                        line_bot_api.reply_message(  
                            event.reply_token,
                            TextSendMessage(text=Insurance.y)
                        )
                    if event.postback.data[1:2] == "C": 
                        line_bot_api.reply_message(  
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Carousel template',
                                template=CarouselTemplate(
                                    columns=[
                                        CarouselColumn(
                                            thumbnail_image_url="https://imgur.com/noUBzWp.jpg",
                                            title="法條檢索",
                                            text="內容提及之法條如下",
                                            actions=[
                                                PostbackTemplateAction(
                                                    label='金融消費者保護法第13條第2項',
                                                    text='金融消費者保護法第13條第2項',
                                                    data='金融消費者保護法第13條第2項'
                                                ),
                                                PostbackTemplateAction(
                                                    label='保險法第54條第2項',
                                                    text='保險法第54條第2項',
                                                    data='law'
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        )

                if event.postback.data[0:1] == "2": 

                    if event.postback.data[1:2] == "A": 
                        line_bot_api.reply_message(  
                            event.reply_token,
                            TextSendMessage(text=Insurance.b)
                        )
                    if event.postback.data[1:2] == "B": 
                        line_bot_api.reply_message(  
                            event.reply_token,
                            TextSendMessage(text=Insurance.x)
                        )

            elif isinstance(event, FollowEvent): # 加入好友事件，創建圖文選單
                line_bot_api.set_default_rich_menu ("richmenu-87b42c61d3386994c28e9ca453c61188")
                line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="歡迎加入好友~~\n可點選菜單與機器人互動\n也可以直接輸入想查詢的內容呦!")
                )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
