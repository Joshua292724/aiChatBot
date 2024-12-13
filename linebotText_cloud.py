from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

line_bot_api = LineBotApi('WxEgHciW6U9qtuR3kV+WLu1rQDn8XA3sGSthrY355JrC4W/haqBjSwm2huras0yoBbF/eLnG0tLUJLIqtKvTY+Pdj9JfTAu+CUwxiN6jTXjDGN8PJfrgr7rintXXRMgiSXw757S6+YwT40kjefDemAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8aec8ce37fd63681cda78728e0033493')

genai.configure(api_key="AIzaSyAd3iEx0-zCaKB5clBkic4UBdNA3j0N6j8")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_prompt=event.message.text
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_prompt)
    result=response.text
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))

if __name__ == '__main__':
    app.run()
