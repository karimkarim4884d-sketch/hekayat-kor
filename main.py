import telebot
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string
import threading
import time

# 1. إعداد البوت (ضع التوكن الخاص بك هنا)
API_TOKEN = '8720735734:AAGgVuHCAvzcDDOpwkmrvomQCYHqE-LMCyA'
bot = telebot.TeleBot(API_TOKEN)

# 2. إعداد تطبيق Flask للموقع
app = Flask(__name__)

# متغير عالمي لتخزين بيانات المباراة وعرضها في الموقع
match_info = {
    "title": "في انتظار الرابط...",
    "score": "0 - 0",
    "status": "لم تبدأ",
    "url": "#"
}

# دالة لجلب البيانات من موقع YSSCORES
def scrape_ysscores(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # استخراج اسم المباراة من العنوان
        title = soup.find('title').text.split('-')[0].strip()
        
        # استخراج النتيجة (افتراضي 0-0 إذا لم توجد)
        score_element = soup.find('div', class_='match-score')
        score = score_element.text.strip() if score_element else "0 - 0"
        
        return {"title": title, "score": score, "url": url}
    except:
        return None

# --- أوامر البوت ---
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "مرحباً يا كريم! أرسل رابط المباراة من YSSCORES لتحديث الموقع فوراً.")

@bot.message_handler(func=lambda message: "ysscores.com" in message.text)
def update_site(message):
    global match_info
    url = message.text
    bot.reply_to(message, "⏳ جاري تحديث الموقع بالبيانات الجديدة...")
    
    data = scrape_ysscores(url)
    if data:
        match_info.update(data)
        match_info["status"] = "مباشر الآن"
        bot.send_message(message.chat.id, f"✅ تم التحديث!\nالمباراة: {data['title']}\nالنتيجة: {data['score']}")
    else:
        bot.reply_to(message, "❌ فشل سحب البيانات من هذا الرابط.")

# --- صفحات الموقع (Flask) ---
@app.route('/')
def index():
    # تصميم بسيط وشيك للموقع (Dark Mode)
    html_template = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>حكايات كورة - بث مباشر</title>
        <style>
            body { background-color: #0f0f0f; color: white; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .card { background: #1a1a1a; padding: 30px; border-radius: 20px; border: 2px solid #ed1c24; text-align: center; width: 80%; max-width: 500px; box-shadow: 0 0 20px rgba(237, 28, 36, 0.2); }
            h1 { color: #ed1c24; margin-bottom: 10px; }
            .score { font-size: 3em; font-weight: bold; margin: 20px 0; color: #fff; }
            .status { background: #ed1c24; padding: 5px 15px; border-radius: 10px; font-size: 0.8em; }
            a { color: #aaa; text-decoration: none; font-size: 0.9em; margin-top: 20px; display: block; }
        </style>
        <meta http-equiv="refresh" content="30"> </head>
    <body>
        <div class="card">
            <h1>حكايات كورة</h1>
            <p>{{ info.title }}</p>
            <div class="score">{{ info.score }}</div>
            <span class="status">{{ info.status }}</span>
            <a href="{{ info.url }}" target="_blank">المصدر: YSSCORES</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, info=match_info)

# تشغيل البوت في الخلفية
def run_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    # بدء تشغيل البوت في Thread منفصل
    threading.Thread(target=run_bot).start()
    # تشغيل موقع Flask
    app.run(host='0.0.0.0', port=5000)
        )
  
