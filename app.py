from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import json
import configparser
import os
from urllib import parse
app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
line_login_id = config.get('line-bot', 'line_login_id')
line_login_secret = config.get('line-bot', 'line_login_secret')
my_phone = config.get('line-bot', 'my_phone')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    print(body)
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]

                if text == "我的名字":
                    payload["messages"] = [getNameEmojiMessage()]
                elif text == "註冊":
                    payload["messages"] = [getLogin()]
                elif text == '心理測驗':
                    your_sum = 0
                    scoring1 = {'A': 0, 'B': 1, 'C': 2, 'D': 3, }
                    question1 = {'question': '1.我覺得想哭', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question2 = {'question': '2.我覺得心情不好', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question3 = {'question': '3.我覺得比以前更容易發脾氣', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question4 = {'question': '4.我覺得胸口悶悶的(心肝頭或胸坎綁綁的)', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question5 = {'question': '5.我覺得不輕鬆、不舒服(不適快)', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question6 = {'question': '6.我覺得身體疲勞虛弱無力', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question7 = {'question': '7.我覺得記憶力不好', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question8 = {'question': '8.我覺得做事時無法專心 ', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question9 = {'question': '9.我覺得想事情或做事時比平常要緩慢', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question10 = {'question': '10.我覺得比較會往壞處想', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question11 = {'question': '11.我覺得想不開、甚至想死', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']                        question12 = {'question': '12.我覺得對什麼事都失去興趣', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question13 = {'question': '13.我覺得身體不舒服', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    question14 = {'question': '14.我覺得自己很沒用', 'answer': ['A.一週內一天以下', 'B.一週內一到二天', 'C.一週內三到四天', 'D.一週內五到七天']}
                    status1 = '您的心已經感冒了，心病需要心藥醫，趕緊到醫院找專業及可信賴的醫師檢查，透過他們的診療與治療，你將不會覺得孤單、無助!'
                    status2 = '現在的你必定感到相當不順心，無法展露笑容，一肚子苦惱及煩悶，連朋友也不知道如何幫你，趕緊找專業機構或醫療單位協助，透過專業機構的協助，必可重拾笑容！!'
                    status3 = '你是不是想笑又笑不太出來，有很多事壓在心上，肩上總覺得很沈重？因為你的壓力負荷量已經到了臨界點了！千萬別再「撐」了！趕快找個有相同經驗的朋友聊聊，給心情找個出口，把肩上的重膽放下，這樣才不會陷入憂鬱症的漩渦。'
                    status4 = '最近的情緒是否起伏不定？或是有些事情在困擾著你？給自己多點關心，多注意情緒的變化，試著瞭解心情變的緣由，做適時的處理，比較不會陷入憂鬱情緒。'
                    status5 = '真是令人羨慕！你目前的情緒狀態很穩定，是個懂得適時調整情緒及抒解壓力的人，繼續保持下去。'

                    getGames(question1, scoring1)
                    getGames(question2, scoring1)
                    getGames(question3, scoring1)
                    getGames(question4, scoring1)
                    getGames(question5, scoring1)
                    getGames(question6, scoring1)
                    getGames(question7, scoring1)
                    getGames(question8, scoring1)
                    getGames(question9, scoring1)
                    getGames(question10, scoring1)
                    getGames(question11, scoring1)
                    getGames(question12, scoring1)
                    getGames(question13, scoring1)
                    getGames(question14, scoring1)

                    if your_sum >= 29:
                        print(status1)
                    elif your_sum >= 19 and your_sum < 29:
                        print(status2)
                    elif your_sum >= 15 and your_sum <= 18:
                        print(status3)
                    elif your_sum >= 9 and your_sum <= 14:
                        print(status4)
                    elif your_sum <= 8:
                        print(status5)
                    else:
                        print('異常狀態請重新測驗')
                    payload["messages"] = [getGames()]                     
                elif text == '專業諮商':
                    payload["messages"] = [getHelp()]
                elif text == "出去玩囉":
                    payload["messages"] = [getPlayStickerMessage()]
                elif text == "台北101":
                    payload["messages"] = [getTaipei101ImageMessage(),
                                           getTaipei101LocationMessage(),
                                           getMRTVideoMessage()]
                elif text == "台北101圖":
                    payload["messages"] = [getTaipei101ImageMessage()]
                elif text == "台北101影片":
                    payload["messages"] = [getMRTVideoMessage()]
                elif text == "quoda":
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": getTotalSentMessageCount()
                            }
                        ]
                elif text == "今日確診人數":
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": getTodayCovid19Message()
                            }
                        ]
                elif text == "主選單":
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "This is a buttons template",
                                "template": {
                                  "type": "buttons",
                                  "title": "Menu",
                                  "text": "Please select",
                                  "actions": [
                                      {
                                        "type": "message",
                                        "label": "我的名字",
                                        "text": "我的名字"
                                      },
                                      {
                                        "type": "message",
                                        "label": "今日確診人數",
                                        "text": "今日確診人數"
                                      },
                                      {
                                        "type": "uri",
                                        "label": "聯絡我",
                                        "uri": f"tel:{my_phone}"
                                      }
                                  ]
                                }
                            }
                        ]
                else:
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": text
                            }
                        ]
                replyMessage(payload)
            elif events[0]["message"]["type"] == "location":
                title = events[0]["message"].get("title", "")
                latitude = events[0]["message"]["latitude"]
                longitude = events[0]["message"]["longitude"]
                payload["messages"] = [getLocationConfirmMessage(title, latitude, longitude)]
                replyMessage(payload)
        elif events[0]["type"] == "postback":
            if "params" in events[0]["postback"]:
                reservedTime = events[0]["postback"]["params"]["datetime"].replace("T", " ")
                payload["messages"] = [
                        {
                            "type": "text",
                            "text": F"已完成預約於{reservedTime}的叫車服務"
                        }
                    ]
                replyMessage(payload)
            else:
                data = json.loads(events[0]["postback"]["data"])
                action = data["action"]
                if action == "get_near":
                    data["action"] = "get_detail"
                    payload["messages"] = [getCarouselMessage(data)]
                elif action == "get_detail":
                    del data["action"]
                    payload["messages"] = [getTaipei101ImageMessage(),
                                           getTaipei101LocationMessage(),
                                           getMRTVideoMessage(),
                                           getCallCarMessage(data)]
                replyMessage(payload)

    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
        )

@app.route("/sendTextMessageToMe", methods=['POST'])
def sendTextMessageToMe():
    pushMessage({})
    return 'OK'

def getLogin():    
    def nextstep():
        member = True
        if member:
            return '請輸入密碼'
        else:
            return '帳號密碼不存在'
    message = {
        'type': 'text',
        'text': '請輸入帳號'}
    nextstep()

    return message and nextstep()

 
def getGames(question, scoring):
    q = question.get('question')
    print(q)
    l = question['answer']
    for allans in l:
        print(allans)
    yourans = input('> ')
    score = scoring.get(yourans.upper())
    if score == None:
        print('您輸入的答案不存在喔')
        getGames(question, scoring)
        return
    global your_sum
    your_sum += score
    your_status = '您的狀態為：\n'
    return your_status                              
                                  

def getGames():
    message = {
      "type": "text",
      "text": "心理測驗",
      "quickReply": {
          "items": [
              {
                "type":"action",
                "imageUrl": "https://example.com/sushi.png",
                "action": {
                  "type": "message",
                  "label": "開心",
                  "text": "開心",
                }
              },
              {
                "type":"action",
                "imageUrl": "https://example.com/sushi.png",
                "action": {
                  "type": "message",
                  "label": "不開心",
                  "text": "不開心",
                }
              }
          ]
          }
        }
    return message


def getHelp():
    message = {
        "type": "template",
        "altText": "this is a carousel template",
        "template": {
            "type": "carousel",
            "columns": [
                {
                    "imageBackgroundColor": "#000000",
                    "title": "諮商心理師公會全國聯合會",
                    "text": "播打:02-2511-8173",
                    "defaultAction": {
                        "type": "uri",
                        "label": "前往首頁",
                        "uri": "https://www.tcpu.org.tw/people-area.html"
                    },
                    "actions": [
                        {
                            "type": "uri",
                            "label": "前往民眾專區",
                            "uri": "https://www.tcpu.org.tw/people-area.html"
                        }
                    ]
                },
                {
                    "imageBackgroundColor": "#000000",
                    "title": "華人心理治療基金會",
                    "text": "播打:02-7700-7866",
                    "defaultAction": {
                        "type": "uri",
                        "label": "前往首頁",
                        "uri": "https://www.tip.org.tw/"
                    },
                    "actions": [
                        {
                            "type": "uri",
                            "label": "我需要面對面諮商",
                            "uri": "https://www.tip.org.tw/f2fbooking"
                        }
                    ]
                },
                {
                    "imageBackgroundColor": "#000000",
                    "title": "國際生命線台灣總會",
                    "text": "播打:1995",
                    "defaultAction": {
                        "type": "uri",
                        "label": "前往首頁",
                        "uri": "http://www.life1995.org.tw/content.asp?id=14"
                    },
                    "actions": [
                        {
                            "type": "uri",
                            "label": "服務項目",
                            "uri": "http://www.life1995.org.tw/content.asp?id=8"
                        }
                    ]
                },
                {
                    "imageBackgroundColor": "#000000",
                    "title": "張老師基金會",
                    "text": "播打:1980",
                    "defaultAction": {
                        "type": "uri",
                        "label": "前往首頁",
                        "uri": "http://www.1980.org.tw/web3-20101110/main.php?customerid=3"
                    },
                    "actions": [
                        {
                            "type": "uri",
                            "label": "使用者專區",
                            "uri": "http://www.1980.org.tw/vlr/login-v3.htm"
                        }
                    ]
                }
            ],
            "imageAspectRatio": "rectangle",
            "imageSize": "cover"
        }
    }
    return message


def getNameEmojiMessage():
    lookUpStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    productId = "5ac21a8c040ab15980c9b43f"
    name = "Miles"
    message = dict()
    message["type"] = "text"
    message["text"] = "".join("$" for r in range(len(name)))
    emojis_list = list()
    for i, nChar in enumerate(name):
        emojis_list.append(
            {
              "index": i,
              "productId": productId,
              "emojiId": f"{lookUpStr.index(nChar) + 1 :03}"
            }
        )
    message["emojis"] = emojis_list
    return message


def getCarouselMessage(data):
    message = {
      "type": "template",
      "altText": "this is a image carousel template",
      "template": {
          "type": "image_carousel",
          "columns": [
              {
                "imageUrl": F"{end_point}/static/taipei_101.jpeg",
                "action": {
                  "type": "postback",
                  "label": "台北101",
                  "data": json.dumps(data)
                }
              },
              {
                "imageUrl": F"{end_point}/static/taipei_1.jpeg",
                "action": {
                  "type": "postback",
                  "label": "台北101",
                  "data": json.dumps(data)
                }
              }
          ]
          }
        }
    return message


def getLocationConfirmMessage(title, latitude, longitude):
    data = {'title': title, 'latitude': latitude, 'longitude': longitude,
            'action': 'get_near'}
    message = {
      "type": "template",
      "altText": "this is a confirm template",
      "template": {
          "type": "confirm",
          "text": f"確認是否搜尋 {title} 附近地點？",
          "actions": [
              {
                 "type": "postback",
               "label": "是",
               "data": json.dumps(data),
               },
              {
                "type": "message",
                "label": "否",
                "text": "否"
              }
          ]
      }
    }
    return message


def getCallCarMessage(data):
    message = {
      "type": "template",
      "altText": "this is a template",
      "template": {
          "type": "buttons",
          "text": f"請選擇至 {data['title']} 預約叫車時間",
          "actions": [
              {
               "type": "datetimepicker",
               "label": "預約",
               "data": json.dumps(data),
               "mode": "datetime"
               }
          ]
      }
    }
    return message


def getPlayStickerMessage():
    message = dict()
    message["type"] = "sticker"
    message["packageId"] = "446"
    message["stickerId"] = "1988"
    return message


def getTaipei101LocationMessage():
    message = dict()
    message["type"] = "location"
    message["title"] = "台北101"
    message["address"] = "110台北市信義區信義路五段7號"
    message["latitude"] = 25.034056468449304
    message["longitude"] = 121.56466736984362
    return message


def getMRTVideoMessage():
    message = dict()
    message["type"] = "video"
    message["originalContentUrl"] = F"{end_point}/static/taipei_101_video.mp4"
    message["previewImageUrl"] = F"{end_point}/static/taipei_101.jpeg"
    return message


def getMRTSoundMessage():
    message = dict()
    message["type"] = "audio"
    message["originalContentUrl"] = F"{end_point}/static/mrt_sound.m4a"
    import audioread
    with audioread.audio_open('static/mrt_sound.m4a') as f:
        # totalsec contains the length in float
        totalsec = f.duration
    message["duration"] = totalsec * 1000
    return message


def getTaipei101ImageMessage(originalContentUrl=F"{end_point}/static/taipei_101.jpeg"):
    return getImageMessage(originalContentUrl)


def getImageMessage(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = originalContentUrl
    message["previewImageUrl"] = originalContentUrl
    return message


def replyMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/reply",headers=HEADER,data=json.dumps(payload))
    return 'OK'


def pushMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/push",headers=HEADER,data=json.dumps(payload))
    return 'OK'


def getTotalSentMessageCount():
    response = requests.get("https://api.line.me/v2/bot/message/quota/consumption",headers=HEADER)
    return response.json()["totalUsage"]


def getTodayCovid19Message():
    response = requests.get("https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN")
    date = response.json()[0]["a04"]
    total_count = response.json()[0]["a05"]
    count = response.json()[0]["a06"]
    return F"日期：{date}, 人數：{count}, 確診總人數：{total_count}"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['POST'])
def upload_file():
    payload = dict()
    if request.method == 'POST':
        file = request.files['file']
        print("json:", request.json)
        form = request.form
        age = form['age']
        gender = ("男" if form['gender'] == "M" else "女") + "性"
        if file:
            filename = file.filename
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(img_path)
            print(img_path)
            payload["to"] = my_line_id
            payload["messages"] = [getImageMessage(F"{end_point}/{img_path}"),
                {
                    "type": "text",
                    "text": F"年紀：{age}\n性別：{gender}"
                }
            ]
            pushMessage(payload)
    return 'OK'


@app.route('/line_login', methods=['GET'])
def line_login():
    if request.method == 'GET':
        code = request.args.get("code", None)
        state = request.args.get("state", None)

        if code and state:
            HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
            url = "https://api.line.me/oauth2/v2.1/token"
            FormData = {"grant_type": 'authorization_code', "code": code, "redirect_uri": F"{end_point}/line_login", "client_id": line_login_id, "client_secret":line_login_secret}
            data = parse.urlencode(FormData)
            content = requests.post(url=url, headers=HEADERS, data=data).text
            content = json.loads(content)
            url = "https://api.line.me/v2/profile"
            HEADERS = {'Authorization': content["token_type"]+" "+content["access_token"]}
            content = requests.get(url=url, headers=HEADERS).text
            content = json.loads(content)
            name = content["displayName"]
            userID = content["userId"]
            pictureURL = content["pictureUrl"]
            statusMessage = content["statusMessage"]
            print(content)
            return render_template('profile.html', name=name, pictureURL=
                                   pictureURL, userID=userID, statusMessage=
                                   statusMessage)
        else:
            return render_template('login.html', client_id=line_login_id,
                                   end_point=end_point)


if __name__ == "__main__":
    app.debug = True
    app.run()

