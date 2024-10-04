from dotenv import load_dotenv
from flask import abort, request, Flask
import os,re

from src.handle import ApiV1

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

load_dotenv()

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("TOKEN"))
handler = WebhookHandler(os.getenv("SECRET"))

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
    if re.match(r'^[e][v][e][n][t][-][a-z]{2}$', event.message.text):
        msg = ApiV1(event.message.text[6:], False)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(msg.get_data())))
    elif re.match(r'^[e][v][e][n][t][-][a-z]{2}[-][0-9]*$', event.message.text):
        msg = ApiV1(event.message.text[6:], True)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(msg.get_data())))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("ERROR")))

if __name__ == "__main__":
    app.run(port=5001)
