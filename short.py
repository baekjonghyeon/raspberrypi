from flask import Flask, request
from flask import render_template
from urllib.parse import urlencode,unquote
import requests
import json
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def home():
	today = datetime.today()
	daystr =str(today.year) + "년" + str(today.month) + "월" + str(today.day) + "일"
	return render_template("index.html", title="my frist Flask",today=daystr)
	
@app.route("/short weather")
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
			,"base_date":"20200622"
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
	app.run(host="0.0.0.0",port="80000")
