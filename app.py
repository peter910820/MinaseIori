import os
import re
from loguru import logger

from dotenv import load_dotenv
from flask import abort, request, Flask

from src.matsurihime import ApiV1

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

load_dotenv()

app = Flask(__name__)
configuration = Configuration(access_token=os.getenv('TOKEN'))
handler = WebhookHandler(os.getenv('SECRET'))


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
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        msg = None

        try:
            if re.match(r'^event-[a-z]{2}$', event.message.text):
                api = ApiV1(event.message.text[6:], False)
                msg = TextMessage(text=str(api.get_data()))  # type: ignore
            elif re.match(r'^event-[-][a-z]{2}[-][0-9]*$', event.message.text):
                api = ApiV1(event.message.text[6:], True)
                msg = TextMessage(text=str(msg.get_data()))  # type: ignore
            else:
                pass

            if msg != None:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        replyToken=event.reply_token,
                        messages=[msg],
                        notificationDisabled=True
                    )
                )
            else:
                pass
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    app.run(port=os.getenv("PORT"))  # type: ignore
