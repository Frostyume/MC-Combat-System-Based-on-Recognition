'''
Author: linin00
Date: 2022-12-13 01:34:09
LastEditTime: 2022-12-13 23:54:35
LastEditors: linin00
Description: 
FilePath: /open/Gesture/core/function.py

'''
import sys
sys.path.append('./Gesture/core')
from mqtt_utils import Mqtt_async
sys.path.append('./Gesture/core/type')
import Topic, Msg
from Gesture import Gesture
from mediapipe_utils import BodyController
from cv2_utils import Camera, waitKey, showImage, FPS, destroy

def my_wearing(body: BodyController, mqtt: Mqtt_async, prefix: str):
  camera = Camera() # 调出摄像头
  fps = FPS() # 打印帧率
  body = BodyController() # 姿态识别
  mqtt.SUB(Topic.ALLREADY)
  while True:
    # 检查是否全部人都穿好了
    msg, topic = mqtt.getMsg()
    if topic == Topic.ALLREADY and msg == Msg.ALLREADY:
      mqtt.UNSUB(Topic.ALLREADY) # 不再订阅
      break
    img = camera.read()
    res = body.process(img)
    if res == Gesture.HEAD:
      mqtt.PUB(Topic.POSE, prefix + Msg.HEAD)     # 头
    elif res == Gesture.LEFTARM:
      mqtt.PUB(Topic.POSE, prefix + Msg.LEFTARM)  # 左臂
    elif res == Gesture.RIGHTARM:
      mqtt.PUB(Topic.POSE, prefix + Msg.RIGHTARM) # 右臂
    elif res == Gesture.LEFTLEG:
      mqtt.PUB(Topic.POSE, prefix + Msg.LEFTLEG)  # 左腿
    elif res == Gesture.RIGHTLEG:
      mqtt.PUB(Topic.POSE, prefix + Msg.RIGHTLEG) # 右腿
    elif res == Gesture.BODY:
      mqtt.PUB(Topic.POSE, prefix + Msg.BODY)     # 躯干
    fps.printFps(img)
    showImage(img)
    waitKey(1, 'q')
  destroy() # 关闭窗口

from speech_utils import Speech
def my_fighting(mqtt: Mqtt_async, prefix: str):
  speech = Speech(mqtt=mqtt, prefix=prefix)
  mqtt.SUB(Topic.GAMEOVER)
  while True:
    msg, topic = mqtt.getMsg()
    if topic == Topic.GAMEOVER and msg == Msg.GAMEOVER:
      mqtt.UNSUB(Topic.GAMEOVER) # 不再订阅，结束游戏
      break
    speech.listen() # 监听键盘任务