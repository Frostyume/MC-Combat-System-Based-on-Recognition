'''
Author: linin00
Date: 2022-12-11 11:58:59
LastEditTime: 2022-12-12 13:59:23
LastEditors: linin00
Description: 
FilePath: /open/Gesture/test/mqtt_server.py

'''
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode("utf-8"))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('dev.linin.xyz', 8302, 600) # 600为keepalive的时间间隔
client.subscribe('fifa', qos=0)
client.loop_forever() # 保持连接