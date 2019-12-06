import RPi.GPIO as GPIO
import requests
import json
from threading import Timer
from time import sleep, strftime
from datetime import datetime

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT


def jprint(obj):
	text = json.dumps(obj, sort_keys=True, indent=4)
	# print(text)
	weather_json = json.loads(text)
	#print(weather_json['current'])
	current_json = weather_json['current'] #Get current info
	temp = current_json['temperature'] #Get current Temparature
	print("Temparature "+str(temp)+"oC")
	show_message(device, "Temparature "+str(temp)+"oC", fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)
	humidity = current_json['humidity']
	print("Humidity "+str(humidity)+"%") #Get current Humidity
	show_message(device, "Humidity "+str(humidity)+"%", fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)
	real_feel = current_json['feelslike']
	print("Real feel "+str(real_feel)+"oC") #Get real feeling
	show_message(device, "Real feel "+str(real_feel)+"oC", fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)
	weather_descript = current_json['weather_descriptions']
	for w in range(len(weather_descript)):
		print("Weather descriptions "+weather_descript[w]) #Weather Descriptions
		show_message(device, weather_descript[w], fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(5)
virtual = viewport(device, width=32, height=16)

# api-endpoint 
URL = "http://api.weatherstack.com/current"

payload = {
	'access_key' : 'xxxxxxxxxxxxxxxxxxxxxxxx',
	'query' : 'Bochum'
}

run_counter = 0
	
while(True):
	now = datetime.now()
	current_min = now.minute
	if current_min == 0 or run_counter == 0: #Change start minute like you want. Here is 0er minute
		response = requests.get(URL, params=payload)
		run_counter+=1
		print(">>>>>>>>>>>Run "+str(run_counter)+"er time.<<<<<<<<<<<<")
		
	if response.status_code == 404:
		print("Not OK!");
	elif response.status_code == 200:
		print("OK. Get data successful...")
		jprint(response.json())
	else:
		print("Error "+str(response.status_code))
