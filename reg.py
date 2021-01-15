import sqlite3
from pyrogram import Client , filters
from pyrogram.types import InlineKeyboardButton , InlineKeyboardMarkup
from time import sleep
import random

api_id = 2669159
api_hash = '761194071ffe6e596a71e72056a9ae73'
bot_token="1586803019:AAHOD0ERKk5307ks25MpQi5o2so24hpPbGY"
app = Client("reg", api_id, api_hash,bot_token)
with app:
    username_bot = "@" + app.get_me().username
DataBase = sqlite3.connect("register-data.db")
cursor = DataBase.cursor()
sendlist = False
chlist = []
chalenge = False
SQ = """
    CREATE TABLE IF NOT EXISTS users(
        userId integer PRIMARY KEY ,
        Fname text,
        userName text
    );
"""

cursor.execute(SQ)
DataBase.commit()
DataBase.close()

userid = ''
username = ''
firstname = ''

@app.on_message(filters.command(["registry", f"registry{username_bot}"]) & filters.group)
def registry(c,m):
    OpenReg = InlineKeyboardMarkup([
                [InlineKeyboardButton('ثبت نام', url='https://t.me/bet_ww_bot/?start=null')]
])
    m.reply("**روی ثبت نام بمال**",
    reply_markup=OpenReg)

@app.on_message(filters.text & filters.group)
def chalenge_list(c,m):
    global userid , username , firstname , chalenge , sendlist
    if "/ch_on" in m.text:
        tim = m.text.split()[1]
        app.send_message(m.chat.id, f"**خب هر {tim} مین قرعه کشی میکنم\n یکی برنده لاتاری میشه \n بنظرت این آدم خوش شانس کیه**")
        chalenge = True
        if chalenge == True:
            while chalenge:
                try:
                    DataBase = sqlite3.connect("register-data.db")
                    cursor = DataBase.cursor()
                    SQlis = "SELECT * FROM users"
                    cursor.execute(SQlis)
                    for b in cursor:
                        iduser = b[0]
                        nameuser = b[1]
                        usname = b[2]
                        mention = f"[{nameuser}](tg://user?id={iduser})"
                        mkds = 'username: ندارد'
                        if usname == 'None' or usname == '':
                            usname = ''
                        else:
                            mkds = f"username: @{usname}"
                        ran = "id: `{}` \nname: {} \n{}".format(iduser,mention,mkds)
                        chlist.append(ran)
                        print(ran)
                    rand = random.choice(chlist)
                    DataBase.commit()
                    DataBase.close()
                    sleep(int(tim)*60)
                    app.send_message(m.chat.id ,f"**برنده این دوره از قرعه کشی کسی نیست جز**\n\n{rand}")
                    chlist.clear()
                except:
                    pass
    if "/ch_off" in m.text:
        chalenge = False
        app.send_message(m.chat.id, "**قرعه کشی خاموش شد**")
    if "/list_on" in m.text:
        time = m.text.split()[1]
        app.send_message(m.chat.id, f"**دریافت لیست هر {time} مین برای گروه فعال شد**")
        sendlist = True
        if sendlist == True:
            while sendlist:
                try:
                    DataBase = sqlite3.connect("register-data.db")
                    cursor = DataBase.cursor()
                    SQlist = "SELECT * FROM users"
                    cursor.execute(SQlist)
                    PM1 = "1- "
                    PM2 = "2- لیست شرکت کنندگان \n"
                    PM3 = "3- لیست شرکت کنندگان \n "
                    msg = "لیست شرکت کنندگان \n"
                    for a in cursor:
                        iduser = a[0]
                        nameuser = a[1]
                        usname = a[2]
                        mention = f"[{nameuser}](tg://user?id={iduser})"
                        mljg = 'username: ندارد'
                        if usname == 'None' or usname == '':
                            usname = ''
                        else:
                            mljg = f"username: @{usname}"
                        if msg:
                            msg += "id: `{}` \nname: {} \n{}\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n".format(iduser,mention,mljg)
                    for uu in msg.split("\n")[0:161]:
                        PM1 += "{}\n".format(uu.split('\n')[0])
                    for gg in msg.split("\n")[161:321]:
                        PM2 += "{}\n".format(gg.split('\n')[0])
                    for ff in msg.split("\n")[321:481]:
                        PM3 += "{}\n".format(ff.split('\n')[0])
                    DataBase.commit()
                    DataBase.close()
                    app.send_message(m.chat.id ,PM1)
                    app.send_message(m.chat.id ,PM2)
                    app.send_message(m.chat.id ,PM3)
                    sleep(int(time)*60)
                except:
                    pass
    if "/list_off" in m.text:
        sendlist = False
        app.send_message(m.chat.id, "**دریافت خودکار لیست غیرفعال شد**")

@app.on_message(filters.command(["start", f"start{username_bot}"]) & filters.private)
def starting(c,m):
    global userid , username , firstname
    user_info = app.get_chat(m.chat.id)
    userid = user_info["id"]
    username = user_info['username']
    mtnakhr = ''
    if username is None:
        username = ''
    else:
        mtnakhr = f"\n**یوزر نیم:** @{username}"
    firstname = user_info["first_name"]
    try:
        if app.get_messages(m.chat.id, [1]):
            DataBase = sqlite3.connect("register-data.db")
            cursor = DataBase.cursor()
            SQI = "INSERT INTO users VALUES ({},'{}','{}');".format(userid,firstname,username)
            cursor.executescript(SQI)
            DataBase.commit()
            DataBase.close()
            app.send_message(m.chat.id,"**شروع فرایند ثبت نام شما**")
            app.send_message(m.chat.id, f"""**کاربر با مشخصات فوق ثبت شد**
**نام کاربر:** {firstname}
**آیدی:** `{userid}`{mtnakhr}""")
            app.send_message(-1001396840436, f"""**کاربر با مشخصات فوق ثبت شد**
**نام کاربر:** {firstname}
**آیدی:** `{userid}`{mtnakhr}""")
    except:
        if app.get_messages(m.chat.id, [2]):
            app.send_message(m.chat.id , "**شما قبلا ثبت نام کرده اید**")
            app.send_message(m.chat.id, f"""**مشخصات شما**
**نام کاربر:** {firstname}
**آیدی:** `{userid}`{mtnakhr}""")

@app.on_message(filters.command(["DeleteMe", f"DeleteMe{username_bot}"]) & filters.private)
def delme(c,m):
    global userid , username , firstname
    user_info = app.get_chat(m.chat.id)
    userid = user_info["id"]
    DataBase = sqlite3.connect("register-data.db")
    cursor = DataBase.cursor()
    SQD = "DELETE FROM users WHERE userId = {}".format(userid)
    cursor.execute(SQD)
    DataBase.commit()
    DataBase.close()
    app.send_message(m.chat.id , "**ثبت نام شما لغو شد**")
app.run()