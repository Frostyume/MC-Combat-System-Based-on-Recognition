'''
Author: linin00
Date: 2022-12-11 11:57:30
LastEditTime: 2022-12-11 12:17:54
LastEditors: linin00
Description: 
FilePath: /open/Gesture/test/mqtt_client.py

'''
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('dev.linin.xyz', 8302, 600) # 600为keepalive的时间间隔
client.publish('fifa', payload='amazing', qos=0)
