from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# دالة سحب البيانات من الموقع الرياضي
def get_match_data():
    # الرابط اللي أنت اخترته كمثال
    url = "https://www.ysscores.com/ar/match/5205734/برشلونة-vs-نيوكاسل"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # محاولة جلب العنوان والنتيجة
        title = soup.find('title').text.split('-')[0].strip()
        # ملاحظة: الكلاسات قد تختلف حسب تحديث الموقع، ده كود احتياطي
        score = "0 - 0" 
        score_elem = soup.find('div', class_='match-score')
        if score_elem:
            score = score_elem.text.strip()
            
        return {"title": title, "score": score, "status": "مباشر الآن"}
    except:
        return {"title": "برشلونة vs نيوكاسل", "score": "جاري التحميل..", "status": "قريباً"}

@app.route('/')
def index():
    data = get_match_data()
    return render_template('index.html', info=data)

if __name__ == '__main__':
    app.run()
  
