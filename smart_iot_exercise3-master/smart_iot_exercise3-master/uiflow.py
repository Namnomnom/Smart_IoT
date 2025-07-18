"""
Filename: uiflow.py
Authors: Matthias Jansa, Nam Nguyen
Date: 2024-11-25
Description: This script receives data from two TOF sensors and sends a mqtt message when a trigger is activated
used sources: built in examples for the TOF sensor and MQTT in UiFLow V.1.13.9
"""
from umqtt.simple import MQTTClient
from m5stack import *
from m5ui import *
from uiflow import *
import time
import unit

# initialize the TOF sensor
setScreenColor(0x000000)
tof0 = unit.get(unit.TOF, unit.PORTA)
tof1 = unit.get(unit.TOF, unit.PORTC)

#TOF port A (inner)
label0 = M5TextBox(160, 0, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
label1 = M5TextBox(270, 0, "mm", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
label2 = M5TextBox(0, 0, "distance#A:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)


#TOF port C (outer)
label3 = M5TextBox(160, 50, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
label4 = M5TextBox(270, 50, "mm", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
label5 = M5TextBox(0, 50, "distance#C:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)



# create a label for the counter
stall_label = M5TextBox(0, 90, "Stall: ", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
labelS = M5TextBox(160, 90, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
# create a label for Trigger port A
tA = M5TextBox(0, 120, "trigger A:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
labelTA = M5TextBox(160, 120, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
# create a label for Trigger port C
tC = M5TextBox(0, 150, "trigger C:", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
labelTC = M5TextBox(160, 150, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)
# create a label for control last
tC = M5TextBox(0, 180, "last ", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
labelTL = M5TextBox(160, 180, "Text", lcd.FONT_DejaVu24, 0x08feab, rotate=0)

# Initialize the counters
checkPortA = 0
checkPortC  = 0
stall = 2

checkLast = 0 # 0 no sensor, 1 -> sensor port A (inner), 2 -> sensor port C (outer)
# RGB-LED-R = TOF / distance 1,5
rgb.setColorFrom(1, 5, 0x000000)
# RGB-LED-L = PIR / movement 6,10
rgb.setColorFrom(6, 10, 0x000000)

# mqtt configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "71680b40"
MQTT_TOPIC = "/sensor/data/SIOT"


# initializing mqtt client
mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
mqtt_client.connect()
print("MQTT verbunden")


while True:
  # set display
  label0.setText(str(tof0.distance))
  label3.setText(str(tof1.distance))
  
  labelS.setText(str(stall))
  labelTA.setText(str(checkPortA))
  labelTC.setText(str(checkPortC))
  labelTL.setText(str(checkLast))
  
  #TOF in port A (inner)
  if (tof0.distance) < 1300:
    # set the RGB-LED-R to blue when triggered
    rgb.setColorFrom(1, 5, 0x000099)
    checkPortA = 1
  else:
    wait_ms(2)
    rgb.setColorFrom(1, 5, 0x009900)
    checkPortA = 0
  

  #TOF in port C (outer)
  if (tof1.distance) < 1300:
    # set the RGB-LED-L to red when triggered
    rgb.setColorFrom(6, 10, 0x990000)
    checkPortC = 1
  else:
    wait_ms(2)
    rgb.setColorFrom(6, 10, 0x009900)
    checkPortC = 0
   
  
  # when A triggers first -> duck leaves the pen
  # when C triggers first -> duck enters the pen
  
  
  # 0 -> none; 1 -> A triggered first; 2 -> C triggered first
  if (checkPortA == 1) and (checkPortC != 1): 
    checkLast = 1
  if checkPortC == 1 and (checkPortA != 1):
    checkLast = 2
  
  
  if checkLast == 1:
    checkLast = 0
    checkPortA = 0
    checkPortC = 0
    if(stall > 0):
      stall -= 1
      # send mqtt message
      message = '{"count": %d}' % (stall)
      mqtt_client.publish(MQTT_TOPIC, message)
      print("Daten gesendet:", message)

    
  if checkLast == 2:
    checkLast = 0
    checkPortA = 0
    checkPortC = 0
    if(stall  < 2):
      stall += 1
      message = '{"count": %d}' % (stall)
      mqtt_client.publish(MQTT_TOPIC, message)
      print("Daten gesendet:", message)
  
  wait_ms(2)