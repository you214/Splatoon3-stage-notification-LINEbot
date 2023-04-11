import os
import json
import requests

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models import (
    FlexSendMessage, BubbleContainer, ImageComponent, TextComponent, BoxComponent, \
    FlexContainer, SeparatorComponent, TextSendMessage
    )

# LINE BotのAPI
line_bot_api = LineBotApi("ENTERYOURKEY")

# スプラトゥーンのステージ情報を取得するURL
URL = "https://spla3.yuu26.com/api/regular/now"

payload ={
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png",
            "position": "relative"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "Stage1",
                "wrap": True,
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "text",
                "text": "ナワバリバトル"
            }
            ],
            "spacing": "sm"
        }
        },
        {
        "type": "bubble",
        "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_6_carousel.png"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "text",
                "text": "Stage2",
                "wrap": True,
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "text",
                "text": "ナワバリバトル"
            }

            ]
        }
        }
    ]
}

def lambda_handler(event, context):
    response = requests.get(URL)
    data = response.json()
    
    payload["contents"][0]["hero"]["url"] = data["results"][0]["stages"][0]["image"]
    payload["contents"][0]["body"]["contents"][0]["text"] = data["results"][0]["stages"][0]["name"]

    payload["contents"][1]["hero"]["url"] = data["results"][0]["stages"][1]["image"]
    payload["contents"][1]["body"]["contents"][0]["text"] = data["results"][0]["stages"][1]["name"]

    flex_message = FlexSendMessage(alt_text="スプラトゥーンのステージ情報", contents=payload)
    try:
        line_bot_api.broadcast(flex_message)
    except LineBotApiError as e:
        # error handle
        print("Failure push message.")
        return {
            'statusCode': 400
        }

    return {
        'statusCode': 200
    }
