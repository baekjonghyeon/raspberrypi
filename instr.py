from flask import Flask, request

from flask import render_template

from urllib.parse import urlencode, unquote

import requests

import json

import datetime

 

 

app= Flask(__name__)

 

@app.route("/")

def home():

	today = datetime.datetime.today()

	daystr = str(today.year) +"년" + str(today.month) +"월"+str(today.day) +"일"

	return render_template("weather.html",pop = result["강수확률"],tmx = result["최고기온"),reh = result["습도"])

 

 

@app.route("/weather")

def weather():

	x = request.values.get("x","error")

	y = request.values.get("y","error")

	if x=="error" or y=="error":

		return "x와 y값을 바르게 입력하시오"

	url= "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"

	qs = "?" + urlencode(

		{

			"serviceKey" : unquote("3rEfTtuHnc7zEvwZewPaH8eQ958F8L6oxXRdFhI7VzfMdGFSwaNNjn6Ivz%2F2ZLpV76Y1eVDT6uTjPmqsrjnqeg%3D%3D")

			,"pageNO" : "1"

			,"numOfRows":"30"

			,"dataType":"JSON"

			,"base_date":"20200622"

			,"base_time": "0500"

			,"nx":x

			,"ny":y

		}

	)

	response=requests.get(url+qs)

	json_weather = json.loads(response.text)

	wth_response = json_weather.get("response")

	wth_body= wth_response.get("body")

	wth_items=wth_body.get("items")

	

	result={'강수확률':0,'최고기온':0,'습도':0}

	

	for wth_item in wth_items.get("item"):

		if wth_item.get("category")=="POP":

			result['강수확률']=wth_item.get("fcstValue")

		elif wth_item.get("category")=="TMX":

			result['최고기온']=wth_item.get("fcstValue")

		elif wth_item.get("category")=="REH":

			result['습도']=wth_item.get("fcstValue")

	return str(result)

	

	

def before_request():

	app.jinja_env.cache = {}	

	

if __name__ == "__main__":

	app.before_request(before_request)

	app.run(host="0.0.0.0",port="8889")
