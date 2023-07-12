'''
Author: linin00
Date: 2022-12-11 11:51:43
LastEditTime: 2022-12-13 03:10:13
LastEditors: linin00
Description: 
FilePath: /open/Gesture/core/mqtt_utils.py

'''

import paho.mqtt.client as mqtt
import json
import time
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode("utf-8"))

class Mqtt:

    def __init__(self, host, post):
        self.host = host
        self.post = post
        self.mqttClient = mqtt.Client()
        self.mqttClient.on_connect = on_connect
        self.mqttClient.on_message = on_message
        self.__connect()

    def __connect(self):
        self.mqttClient.connect(self.host, self.post, 60)
        # self.mqttClient.loop_start()

    def PUB(self, topic, payload, qos=1):
        """发布信息"""
        self.mqttClient.publish(topic, payload, qos)

    def SUB(self, topic, qos=1):
        """订阅频道"""
        self.mqttClient.subscribe(topic, qos)
        self.mqttClient.loop_forever()

# 异步通信模型
# 使用线程安全的队列保证接收的消息不会丢失
from queue import Queue
class Mqtt_async:

    def __init__(self, host, post):
        self.host = host
        self.post = post
        self.mqttClient = mqtt.Client()
        self.mqttClient.on_connect = on_connect
        self.mqttClient.on_message = self.__on_message
        self.msg = Queue(maxsize=1024)
        self.__connect()
    def __on_message(self, client, userdata, msg):
        # print(msg.topic, msg.payload.decode("utf-8"))
        self.msg.put(msg)
    def __connect(self):
        self.mqttClient.connect(self.host, self.post, 60)
        self.mqttClient.loop_start()

    def PUB(self, topic, payload, qos=1):
        """发布信息"""
        self.mqttClient.publish(topic, payload, qos)
        time.sleep(0.5)
    def SUB(self, topic, qos=1):
        """订阅频道"""
        self.mqttClient.subscribe(topic, qos)
    def UNSUB(self, topic):
        """取消订阅"""
        self.mqttClient.unsubscribe(topic)

    def getMsg(self):
        if not self.msg.empty():
            msg = self.msg.get()
            return msg.payload.decode("utf-8"), msg.topic
        return None, None
