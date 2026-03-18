from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# --- بياناتك اللي بعتها يا زاك ---
BOT_TOKEN = "8720735734:AAGgVuHCAvzcDDOpwkmrvomQCYHqE-LMCyA"
ADMIN_ID = "1180877835"

@app.route('/')
def index():
    # بيانات المباراة (تقدر تغيرها من هنا في أي وقت)
    live_match = {
        "title": "برشلونة vs نيوكاسل",
        "score": "2 - 1",
        "status": "مباشر"
    }
    return render_template('index.html', info=live_match)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    user_phone = request.form.get('user_phone')
    screenshot = request.files.get('screenshot')

    if user_phone and screenshot:
        # الرسالة اللي هتوصلك على التليجرام
        caption = f"🔔 عملية اشتراك جديدة في Zack Cinema!\n\n📱 رقم العميل: {user_phone}\n✅ يرجى مراجعة صورة التحويل."
        
        # إرسال الصورة والبيانات للبوت بتاعك
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {'photo': ('screenshot.jpg', screenshot.read(), 'image/jpeg')}
        data = {'chat_id': ADMIN_ID, 'caption': caption}
        
        try:
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                return "<h1>✅ تم إرسال طلبك بنجاح! سيتم مراجعة الدفع وتفعيل حسابك خلال دقائق.</h1>"
            else:
                return f"<h1>❌ فشل الإرسال. تأكد من تشغيل البوت أولاً (اضغط Start في البوت).</h1>"
        except Exception as e:
            return f"<h1>⚠️ حدث خطأ فني: {str(e)}</h1>"

    return "<h1>⚠️ بيانات ناقصة، يرجى ملء الخانات ورفع الصورة.</h1>"

if __name__ == '__main__':
    app.run()
    
