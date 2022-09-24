from flask import Flask, request, abort
import os,re

from src.handle import spider,event_data,preprocessing

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)


line_bot_api = LineBotApi("ROh5//UBYjitP0iq9YUHRd/Is8/IyflOkD1k9FdCTNm9y0GJ5Gdb2zIJ2a7kAjS09aXd/R2nal1KzIwruUyPUuiOiroUk5gnaClajEvlpzBubGLQI8EQVzzVyduj3JrCwOdht+dv3susMPLZOSsGKAdB04t89/1O/w1cDnyilFU=")

handler = WebhookHandler("dccf14eb2af50891e68802225ce51583")


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # msg= []
    if re.match(r'^[e][v][e][n][t][-][a-z]{2}$', event.message.text):
        eventData = event_data()
        print(eventData)
        opt = preprocessing(event.message.text[6:],eventData)
        output = spider(opt, eventData)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(output)))
    elif re.match(r'^[e][v][e][n][t][-][a-z]{2}[-][0-9]*$', event.message.text):
        eventData = event_data()
        # msg.append(TextSendMessage(text=f'Test!!!你的訊息是:{event.message.text}'))
    # line_bot_api.reply_message(event.reply_token, messages=msg[:5])

if __name__ == "__main__":
    app.run()
