import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import schedule
import twitter
import tweepy

   
url = "https://tenki.jp/forecast/3/16/4410/13220/3hours.html"
#HTML取得
res = requests.get(url)
#HTMLのツリー化
soup = BeautifulSoup(res.text, 'html.parser')
#天気気表まで取る
forecast = []    
forecast = soup.select_one("#forecast-point-3h-today")
print(forecast)

CONSUMER_KEY = "wLQRdoh6C64hdnPOa4DthAanR"
CONSUMER_SECRET = "4rn80p3dCjVxZFXoWYqHjfSgnJSLGEObYZJmnpAi0sd1OdMSOB"
ACCESS_TOKEN = "1292458764084240390-hHnbelH172kbcloDVbIazeXLPerg5c"
ACCESS_TOKEN_SECRET = "UiS5nUn6rue7SJ7Wu8mtquj70tJX8IW2wcPXfjYvugRS3"

print("大和市桜ケ丘")

def day():
    day_class = forecast.find(class_="head")
    day_tag = day_class.find("p")
    day_original = day_tag.text
    global month
    month = day_original[3:5]
    global day
    day = day_original[6:8]
    global yobi
    yobi = day_original[9:12]
    print(month)
    print(day)
    print(yobi)

def temperature():
    #temperatureクラスまで取得
    temp_class = forecast.find(class_="temperature")
    
    #print(temp_class)
    #９時から１８時までの気温を取得    
    first_temp = temp_class.find("td")
    second_temp = first_temp.find_next_sibling("td")
    third_temp = second_temp.find_next_sibling("td")
    forth_temp = third_temp.find_next_sibling("td")
    fifth_temp = forth_temp.find_next_sibling("td")
    sixth_temp = fifth_temp.find_next_sibling("td")
    
    global three_temp_str
    three_temp_str = [third_temp.text, fifth_temp.text, sixth_temp.text]
    
    three_temp_num = list(map(float, three_temp_str))#浮動小数点型に変更


    #平均算出
    temp_avelage = sum(three_temp_num) / 3
    
    #上着の判断
    global wear
    if temp_avelage < 20.0:
        wear = "上着推奨"
    else:
        wear = "半袖OK"
        
    print(three_temp_num)
    print(temp_avelage)
    print(wear)

def amount_of_rain():
    #precipitationクラスまで取得
    rain_class = forecast.find(class_="precipitation")
    #print(rain_class)
    #９時から１８時の降水量を取得
    first_rain = rain_class.find("td")
    second_rain = first_rain.find_next_sibling("td")
    third_rain = second_rain.find_next_sibling("td")
    forth_rain = third_rain.find_next_sibling("td")
    fifth_rain = forth_rain.find_next_sibling("td")
    sixth_rain = fifth_rain.find_next_sibling("td")
    
    global three_rain_str
    three_rain_str = [third_rain.text, fifth_rain.text, sixth_rain.text]
    three_rain_num = list(map(int, three_rain_str))#整数型に変更

    third_rain = three_rain_num[0]
    fifth_rain = three_rain_num[1]
    sixth_rain = three_rain_num[2]
    
    #最大降水量
    max_rain = max(three_rain_num)
    #print(max_rain)
    
    #判断
    global rain_gear
    if max_rain < 1:
        rain_gear = "晴れ"
    elif max_rain <= 2:
        rain_gear = "濡れる"
    elif 2 < max_rain < 5 :
        rain_gear = "雨具必須"
    elif 5 <= max_rain < 10:
        rain_gear = "フル装備必須"
    elif 10 <= max_rain < 20:
        rain_gear = "超降ってる"
    elif 20 <= max_rain < 30:
        rain_gear = "大雨注意報レベル"
    else:
        rain_gear = "大雨警報レベル,STAY HOME!"

    print(three_rain_num)
    print(rain_gear)

def wind_vector():
    wind_vector_class = forecast.find(class_="wind-direction")
    #print(wind_vector_class)



    first_wind_vector = wind_vector_class.find("td")
    second_wind_vector = first_wind_vector.find_next_sibling("td")
    third_wind_vector = second_wind_vector.find_next_sibling("td")
    forth_wind_vector = third_wind_vector.find_next_sibling("td")
    fifth_wind_vector = forth_wind_vector.find_next_sibling("td")
    sixth_wind_vector = fifth_wind_vector.find_next_sibling("td")
    
    global three_wind_vector
    three_wind_vector = [first_wind_vector.text + ";;;", fifth_wind_vector.text + "]]]", sixth_wind_vector.text + ":::"]
    
    global first_wind_vector_str
    first_wind_vector_str = three_wind_vector[0]
    global second_wind_vector_str
    second_wind_vector_str = three_wind_vector[1]
    global third_wind_vector_str
    third_wind_vector_str = three_wind_vector[2]


    
    
    print(" " + first_wind_vector_str, second_wind_vector_str, third_wind_vector_str)

def wind_power():
    wind_power_class = forecast.find(class_="wind-speed")
    #print(wind_power_class)

    
    first_wind_power = wind_power_class.find("td")
    second_wind_power = first_wind_power.find_next_sibling("td")
    third_wind_power = second_wind_power.find_next_sibling("td")
    forth_wind_power = third_wind_power.find_next_sibling("td")
    fifth_wind_power = forth_wind_power.find_next_sibling("td")
    sixth_wind_power = fifth_wind_power.find_next_sibling("td")

    global three_wind_power_str
    three_wind_power_str = [first_wind_power.text, fifth_wind_power.text, sixth_wind_power.text]
    global three_wind_power_num
    three_wind_power_num = list(map(int, three_wind_power_str))#整数型に変更
    print(three_wind_power_num)

    speed = three_wind_power_num[0]
    if max(three_wind_power_num) > 10:
        speed = max(three_wind_power_num)
    
    global coment
    if speed < 2:
        coment = "ほぼ無風"
    elif speed == 2 or speed == 3:
        coment = "ほぼ快適"
    elif speed == 4:
        coment = "早めに"
    elif speed == 5:
        coment = "しんどい"
    elif speed == 6:
        coment = "超しんどい"
    elif speed < 9:
        coment = "全然進まない"
    elif speed <16:
        coment = "あきらめ＜注意報レベル＞"
    elif speed < 24:
        coment = "<台風レベル,暴風警報レベル>"
    else:
        coment = "<外出危険>"

    print(coment)


def need():
    city = [74, 85, 99, 114, 132, 151, 173, 196, 220, 246, 276, 306, 339, 373, 410, 448]
    road = [58, 70, 82, 98, 114, 133, 153, 175, 200, 225, 253, 282, 314, 347, 382, 419]

    global city_job
    global road_job
    city_job = str(city[three_wind_power_num[0]] - 100)
    road_job = str(road[three_wind_power_num[0]] - 100)


    print(city_job)
    print(road_job)

def send():
    # tweepyの設定（認証情報を設定）
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # tweepyの設定（APIインスタンスの作成）
    api = tweepy.API(auth)

    
    
    api.update_status("大和市桜ケ丘" + month + "月" + day + "日" + yobi + "\n"
                    + "時間" + "___気温" + "__降水量" + "__風速" + "___風向\n"
                    + " 9時" + "　  " + three_temp_str[0] + "        " + three_rain_str[0] + "　　　" + three_wind_power_str[0] + "　　" + three_wind_vector[0] + "\n"
                    + "15時" + "　" + three_temp_str[1] + "　　 " + three_rain_str[1] + "　　　" + three_wind_power_str[1] + "　　" + three_wind_vector[1] + "\n"
                    + "18時" + "　" + three_temp_str[2] + "　　 " + three_rain_str[2] + "　　　" + three_wind_power_str[2] + "　　" + three_wind_vector[2] + "\n"
                    + "<コメント>\n" + rain_gear + "("  + wear + ")\n" + coment + "\n" + "　" + city_job + "（ママチャリ）\n" + "　" + road_job + "（ロード）\n")
    
    
def job():
    day()
    time.sleep(1)
    temperature()
    time.sleep(1)
    amount_of_rain()
    time.sleep(1)
    wind_vector()
    time.sleep(1)
    wind_power()
    need()
    send()


job()
