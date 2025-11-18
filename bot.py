# telegram_bot

import telebot
import requests
import random
import os

# ===================== BOT TOKEN =====================
TOKEN = "توکن_ربات_تو_اینجا_قرار_بده"
bot = telebot.TeleBot(TOKEN)

# ===================== MODES =====================
current_mode = "normal"
available_modes = ["normal", "funny", "dark", "coder", "friendly"]

# ===================== RESPONSES =====================
funny_responses = [
    "😂 اوه باز تویی؟ ببینم چی میخوای امروز!",
    "بابا دارم چت می‌کنم، یهو پریدی 😭",
    "عهععع! صدا کردی منو؟ حاضررر 😎",
]

dark_responses = [
    "😐 حرفتو کوتاه بزن.",
    "اگه میخوای جواب بگیری درست حرف بزن.",
    "امشب مود خوب ندارم، ولی بپرس…"
]

friendly_responses = [
    "سلام رفیق خوبم ❤️ چطور کمکت کنم؟",
    "با منی؟ اینجام برات 🌟",
    "اوه سلام دلم تنگ شده بود 😍"
]

normal_responses = [
    "باشه بگو چی میخوای 😎",
    "گوش میدم...",
    "اوکی ادامه بده."
]

# ===================== CODER MODE =====================
def coder_answer(user_msg):
    common_codes = {
        "loop": "for i in range(10):\n    print(i)",
        "if": "x = 10\nif x > 5:\n    print('x بزرگه')",
        "class": "class Person:\n    def __init__(self,name):\n        self.name=name"
    }

    for key in common_codes:
        if key in user_msg.lower():
            return f"این یه نمونه کد ساده برای {key}:\n\n```python\n{common_codes[key]}\n```"

    illegal = ["ddos", "hack wifi", "rat", "keylogger", "bruteforce"]
    for bad in illegal:
        if bad in user_msg.lower():
            return "این کار غیرقانونیه 😐 ولی یادگیری امن سایبری خوبه…"

    return "کدی که میخوای رو درست توضیح بده تا برات بنویسم رفیق 😎"

# ===================== FEATURES =====================
def get_fact():
    try:
        data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        return data["text"]
    except:
        return "فکت پیدا نکردم!"

def get_news():
    try:
        r = requests.get("https://newsdata.io/api/1/news?apikey=pub_12817&language=fa")
        data = r.json()["results"][0]
        return f"{data['title']}\n\n{data['link']}"
    except:
        return "نتونستم خبری بیارم!"

def web_search(q):
    try:
        data = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json").json()
        return data["Abstract"] or "چیزی پیدا نکردم."
    except:
        return "مشکل در سرچ!"

def prank_scan(user):
    return f"""
🔍 اسکن کاربر **{user}** شروع شد...

✔ پیدا کردن پورت‌ها  
✔ جمع‌آوری دیتای سطحی  
✔ بررسی امنیت  
✔ نتیجه: 🤣 پرنک بود، آروم باش!
"""

# ===================== COMMANDS =====================
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "سلام 😎 ربات روشنه بگو چی میخوای؟")

@bot.message_handler(commands=['mode'])
def mode_list(msg):
    bot.reply_to(msg, f"مودهای موجود:\n{', '.join(available_modes)}\n\nبرای تغییر بزن: /setmode funny")

@bot.message_handler(commands=['setmode'])
def set_mode(msg):
    global current_mode
    new_mode = msg.text.replace("/setmode ", "").strip().lower()
    if new_mode in available_modes:
        current_mode = new_mode
        bot.reply_to(msg, f"مود تغییر کرد به: {new_mode} 😎")
    else:
        bot.reply_to(msg, "این مود وجود نداره رفیق.")

@bot.message_handler(commands=['fact'])
def fact_handler(msg):
    bot.reply_to(msg, get_fact())

@bot.message_handler(commands=['news'])
def news_handler(msg):
    bot.reply_to(msg, get_news())

@bot.message_handler(commands=['search'])
def search_handler(msg):
    query = msg.text.replace("/search ", "").strip()
    bot.reply_to(msg, web_search(query))

@bot.message_handler(commands=['scan'])
def scan_handler(msg):
    bot.reply_to(msg, prank_scan(msg.from_user.first_name))

# ===== اضافه: دستور /promo =====
@bot.message_handler(commands=['promo'])
def promo(msg):
    bot.reply_to(
        msg,
        "🔥 رفیق یه نگاه به پیج ما بنداز، دیگه خودت می‌فهمی چرا می‌گم بهترینه 😎👇\n\n"
        "https://t.me/o0Night_Tales0o"
    )

# ===================== MAIN CHAT =====================
@bot.message_handler(func=lambda m: True)
def chat(msg):
    global current_mode
    user_text = msg.text

    if current_mode == "funny":
        bot.reply_to(msg, random.choice(funny_responses))
    elif current_mode == "dark":
        bot.reply_to(msg, random.choice(dark_responses))
    elif current_mode == "friendly":
        bot.reply_to(msg, random.choice(friendly_responses))
    elif current_mode == "coder":
        bot.reply_to(msg, coder_answer(user_text))
    else:
        bot.reply_to(msg, random.choice(normal_responses))

# ===================== RUN BOT =====================
bot.infinity_polling()