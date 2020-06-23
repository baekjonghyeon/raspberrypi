from flask import Flask, request
from flask import render_template
from urllib.parse import urlencode,unquote
from datetime import datetime
import requests
import json
import pymysql

app = Flask(__name__)
db = pymysql.connect(host = 'localhost', user = 'root',password='1234',db='weather',charset='utf8')

@app.route("/")
def home():
	today = datetime.today()
	daystr =str(today.year) + "년" + str(today.month) + "월" + str(today.day) + "일"
	return render_template("index.html", title="my frist Flask",today=daystr)

@app.route("/local")
def local():
	cur = db.cursor()
	cur.execute("Select distinct level3,x,y From localxy Where level2='원주시' and level3 != ''")
	rows = cur.fetchall()
	dongs = []
	
	for row in rows:
		dong = []
		dong.append(row[0])
		dong.append(row[1])
		dong.append(row[2])
		dongs.append(dong)
	print(dongs)
	return render_template("local.html", dong_list = dongs)
		
		#dongs.append(row[0])
		#nxs.append(row[1])
		#nys.append(row[2])
	#return render_template("local.html", dong_list = dongs, nx_list = nxs, ny_list = nys)

@app.route("/weather")
def weather():
	dong = request.values.get("dong","error")
	x = request.values.get("x","error")
	y = request.values.get("y","error")
	if x=="error" or y=="error":
		return" x,y의 값"
	url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"
	qs = "?" + urlencode(
		{
			"serviceKey":unquote("twzSTZ9hlKCyIjDLs9%2FL7aqF7YU6Jf%2BwDccQZG6NfDNC%2BdJU7OPIx0RTckrh5USoV5bBdpUVu1j7xwM%2BZrTl5Q%3D%3D")
			,"pageNo":"1"	
			,"numOfRows":"30"
			,"dataType":"JSON"
			,"base_date":"20200623"
			,"base_time":"0500"
			,"nx":x
			,"ny":y
		}
	)

	response = requests.get(url + qs)
	json_weather = json.loads(response.text)
	wth_response = json_weather.get("response")
	wth_body= wth_response.get("body")
	wth_items=wth_body.get("items")
	
	result = {'강수확률':0,'최고기온':0,'습도':0}
	for wth_item in wth_items.get("item"):
		if wth_item.get("category") =="POP" :
			result['강수확률']=wth_item.get("fcstValue")
		elif wth_item.get("category") =="TMX" :
			result['최고기온']=wth_item.get("fcstValue")
		elif wth_item.get("category") =="REH" :
			result['습도']=wth_item.get("fcstValue")
	return render_template("weather.html",dong=dong, pop = result['강수확률'], tmx = result['최고기온'], reh = result['습도'])

@app.route("/shortweather")
def shortweather():
	x = request.values.get("x","error")
	y = request.values.get("y","error")
	if x=="error" or y=="error":
		return" x,y의 값"
	url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst"
	qs = "?" + urlencode(
		{
			"serviceKey":unquote("twzSTZ9hlKCyIjDLs9%2FL7aqF7YU6Jf%2BwDccQZG6NfDNC%2BdJU7OPIx0RTckrh5USoV5bBdpUVu1j7xwM%2BZrTl5Q%3D%3D")
			,"pageNo":"1"	
			,"numOfRows":"30"
			,"dataType":"JSON"
			,"base_date":"20200623"
			,"base_time":"0500"
			,"nx":x
			,"ny":y
		}
	)

	response = requests.get(url + qs)
	json_weather = json.loads(response.text)
	wth_response = json_weather.get("response")
	wth_body= wth_response.get("body")
	wth_items=wth_body.get("items")
	result = {'기온':0,'1시간 강수량':0,'하늘상태':0,'동서바람성분':0,'남북바람성분':0}
	for wth_item in wth_items.get("item"):
		if wth_item.get("category") =="T1H" :
			result['기온']=wth_item.get("fcstValue")
		elif wth_item.get("category") =="RN1" :
			result['1시간 강수량']=wth_item.get("fcstValue")
		elif wth_item.get("category") =="SKY" :
			result['하늘상태']=wth_item.get("fcstValue")
		elif wth_item.get("category") =="UUU" :
			result['동서바람성분']=wth_item.get("fcstValue")
		elif wth_item.get("category") =="VVV" :
			result['남북바람성']=wth_item.get("fcstValue")
	return render_template("shortweather.html",t1h = result['기온'], rn1 = result['1시간 강수량'], sky = result['하늘상태'],uuu = result['동서바람성분'],vvv = result['남북바람성분'])
	
def before_request():
	app.jinja_env.cache = {}
	
if __name__ == "__main__":
	app.before_request(before_request)
	app.run(host="0.0.0.0",port="8000")
