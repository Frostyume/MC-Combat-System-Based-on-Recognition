'''
Author: linin00
Date: 2022-12-12 14:00:32
LastEditTime: 2022-12-12 23:57:22
LastEditors: linin00
Description: 
FilePath: /open/Gesture/test/mqtt_pub.py

'''
import sys
sys.path.append('Gesture/core')
from mqtt_utils import Mqtt
import time

if __name__ == '__main__':
  # mqtt = Mqtt('dev.linin.xyz', 8302)
  # mqtt.PUB('LJ', 'testing')
  from mqtt_utils import Mqtt_async
  mqtt = Mqtt_async('dev.linin.xyz', 8302)
  for i in range(0, 1000):
    mqtt.PUB('LJ', i)
  time.sleep(1)