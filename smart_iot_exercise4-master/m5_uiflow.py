
""" 
Filename: m5-uiflow.py 
Author: Matthias Jansa, Patrick Meyer
Version: 2.3
Description: This script receives data from the 2xToF and changes a Light when they get triggered and a counter. 
used sources: 
UIFlox (https://flow.m5stack.com/) PIR Load Example/ prior Version 
Chatgpt for time-triggers and Event-trigger
first semester project
utime library for micropython documentation (https://docs.micropython.org/en/v1.15/library/utime.html)
UIFLow documentation (https://docs.m5stack.com/en/uiflow/blockly/hardwares/rtc)
"""
from umqtt.simple import MQTTClient
from m5stack import *
from m5ui import *
from uiflow import *
from m5stack_ui import *
import time
import unit
import urequests
import utime

# initializes the system time to gmt +2 (cet wintertime)
rtc.settime('ntp', host='de.pool.ntp.org', tzone=2)

# initialize the TOF-Sensor
setScreenColor(0x000000)
tof0 = unit.get(unit.TOF, unit.PORTA)
tof1 = unit.get(unit.TOF, unit.PORTC)

# initialize the PIR-Sensor
pir0 = unit.get(unit.PIR, unit.PORTB)

#initializes the mqtt
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "71680b40"
MQTT_TOPIC = "/sensor/data/SIOT"
mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
mqtt_client.connect()
print("MQTT verbunden")

#labels TOF #1
label0 = M5TextBox(160, 0, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
label1 = M5TextBox(270, 0, "mm", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
label2 = M5TextBox(0, 0, "distance#A:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)

#labels TOF #2
label3 = M5TextBox(160, 30, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
label4 = M5TextBox(270, 30, "mm", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
label5 = M5TextBox(0, 30, "distance#C:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
#labels PIR
label6 = M5TextBox(0, 60, "movement:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
labelTM = M5TextBox(160, 60, "False", lcd.FONT_DejaVu24, 0x08feab, rotate=0)



#  creates Label for the pen
pen_label = M5TextBox(0, 90, "pen:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
labelp = M5TextBox(160, 90, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
# creates Label for the Trigger A
tA = M5TextBox(0, 120, "trigger A:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
labelTA = M5TextBox(160, 120, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
# creates Label for the Trigger C
tC = M5TextBox(0, 150, "trigger C:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
labelTC = M5TextBox(160, 150, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
# creates Label for control last
tC = M5TextBox(0, 180, "last ", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
labelTL = M5TextBox(160, 180, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)

#initializes the used variables
trigger_movement = 0
last_trigger_time_A = 0 #when was trigger A last used, based on chatgpt
last_trigger_time_C = 0 #when was trigger C last used based on chatgpt
last_trigger_label = "None"  # saves which sensor tiggered last, based on chatgpt
trigger_window = 3000  # triggerwindow in milliseconds, based on chatgpt
event_processed = False  # to check if a check/action was already done, based on chatgpt
sunset_check = 0 # check if the sunset_time is reached
resettrigger = 0 # to reset the trigger
pen = 2

#initializes the lights
#RGB-LED-L = TOF PortA / distance 1,5
rgb.setColorFrom(1, 5, 0x000000)
#RGB-LED-R = Tof PORTC / distance 6,10
rgb.setColorFrom(6, 10, 0x000000)

# checking the sunset time
api_key = "f15f5d6b8c570d2752ff04ef97259674"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

city_name = "wolfenbüttel"
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric" + "&lang=de"

try:
    label0.setText("request send...")
    response = urequests.get(complete_url)
    label0.setText("request return")    
    x = response.json()  # parsed JSON data from the response
        
    if x["cod"] != "404":  # check if data is valid        
        sunset = x["sys"]["sunset"]        
        # transform unix timestamp to a tuple (year, month, mday, hour, minute, second, weekday, yearday)
        time_tuple = utime.localtime(sunset)
        #normally adding one hour for time difference to UTC, utime.localtime should be CET but gives UTC
        hour = time_tuple[3] # not adding one hour because we want to set the treshhold for alerst to prior the sunset
        minutes = time_tuple[4]
        sunset_total_minutes = hour * 60 + minutes               
    else:
        label0.setText("city not found")
except Exception as e:
    label0.setText("Error: %s" % (e))
finally:
    response.close()  # Ensure the response is properly closed

#start of measurments
while True:
    #read the ToF sensor
    distance_A = tof0.distance
    distance_C = tof1.distance

    # Labels refresh
    label0.setText(str(distance_A))
    label3.setText(str(distance_C))
    labelp.setText(str(pen))
    labelTA.setText(str(last_trigger_time_A)) 
    labelTC.setText(str(last_trigger_time_C)) 
    labelTL.setText(last_trigger_label)

    # check if sunset time is reached
    current_total_minutes = rtc.datetime()[4] *60 + rtc.datetime()[5]  
    if current_total_minutes >= sunset_total_minutes:
        sunset_check = 1

    # time in ms since the system start
    time_since_start = time.ticks_ms()

    # Sensor A control #trigger_time
    if distance_A < 1300:
        #checks whether sensor A was triggered at all or enough time has passed since the last event was triggered by sensor A   
        if last_trigger_time_A == 0 or time.ticks_diff(time_since_start, last_trigger_time_A) > trigger_window:
            last_trigger_time_A = time_since_start
            last_trigger_label = "A"
            event_processed = False  # reset event to prevent multiple incrementation/decrementation of pen-counter
            rgb.setColorFrom(1, 5, 0x000099)  # blue, right side
    else:
        rgb.setColorFrom(1, 5, 0x009900)

    # Sensor C control #trigger_time
    if distance_C < 1300:
        if last_trigger_time_C == 0  or time.ticks_diff(time_since_start, last_trigger_time_C) > trigger_window:
            last_trigger_time_C = time_since_start
            last_trigger_label = "C"
            event_processed = False 
            rgb.setColorFrom(6, 10, 0x990000)  # red, left side
    else:
        rgb.setColorFrom(6, 10, 0x009900)

    # checking Sensor PIR 
    if (pir0.state) == 1:
        labelTM.setText("True")
        trigger_movement = 1
    else:
        labelTM.setText("False")
        trigger_movement = 0     
        
    # checks if A or C got triggered and in which order, event and time
    if not event_processed:  # Checks if an event already happened during this while-run
      if resettrigger == 1: #global reset
          last_trigger_time_A = 0
          last_trigger_time_C = 0
          last_trigger_label = "0"
          event_processed = True
          resettrigger = 0
      else:
        #checks if c has been triggered after a and if a has been triggered at all.
        if last_trigger_time_C > last_trigger_time_A and last_trigger_time_A > 0:
            #to keep the counter between 0 and 2
            if pen <= 1: 
              pen += 1
            # Prevent immediate retriggering by introducing a delay based on chatgpt
            time.sleep_ms(trigger_window // 10)  
            resettrigger = 1
            # Send MQTT message
            message = '{"count": %d, "sunset_check": %d, "movement": %d}' % (pen, sunset_check, trigger_movement)
            mqtt_client.publish(MQTT_TOPIC, message)
            print("Daten gesendet:", message)
        elif last_trigger_time_A > last_trigger_time_C and last_trigger_time_C > 0:
            if pen >= 1:
              pen -= 1
            time.sleep_ms(trigger_window // 10)  
            resettrigger = 1
            message = '{"count": %d, "sunset_check": %d, "movement": %d}' % (pen, sunset_check, trigger_movement)
            mqtt_client.publish(MQTT_TOPIC, message)
            print("Daten gesendet:", message)
      
    wait_ms(2) #wait_ms is from uiflow time.sleep_ms is overall python