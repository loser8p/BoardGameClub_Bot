from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google_sheets
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/api/callback", methods=['POST'])
def callback():
    # 获取X-Line-Signature请求头
    signature = request.headers['X-Line-Signature']

    # 获取请求体
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 验证请求并处理
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.split(',')
    google_sheets.append_row(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='数据已保存至Google Sheets!')
    )

if __name__ == "__main__":
    app.run()
