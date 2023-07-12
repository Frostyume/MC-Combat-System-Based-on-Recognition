'''
Author: linin00
Date: 2022-12-07 18:45:02
LastEditTime: 2022-12-13 23:22:32
LastEditors: linin00
Description: 
FilePath: /open/Gesture/core/mediapipe_utils.py

'''
import cv2
import mediapipe as mp
import numpy as np
import sys
sys.path.append('./Gesture/core/type')
from Gesture import Gesture
import math

# 手部识别
class HandDetector():
  def __init__(self,
              mode=False,
              maxHands=1,
              minDetectionConfidence=0.5,
              minTrackingConfidence=0.5): # 默认识别一只手
    self.__mpHands = mp.solutions.hands
    self.__hands = self.__mpHands.Hands(
      static_image_mode=mode,
      max_num_hands=maxHands,
      min_detection_confidence=minDetectionConfidence,
      min_tracking_confidence=minTrackingConfidence
    )
    self.__mpDraw = mp.solutions.drawing_utils

  def findHands(self, img, draw = True): # 识别手部关键点，默认在传入的图片上画出来
    imRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    self.__results = self.__hands.process(imRGB)
    if draw and self.__results.multi_hand_landmarks :
      for handsLms in self.__results.multi_hand_landmarks :
        self.__mpDraw.draw_landmarks(img, handsLms, self.__mpHands.HAND_CONNECTIONS)

  def trackLandmark(self, img, index, draw = True): # 跟踪某一个关键点坐标，默认在传入的图片上画出来，返回值是关键点的像素坐标
    res = []
    if self.__results.multi_hand_landmarks :
      for handsLms in self.__results.multi_hand_landmarks :
        for id, lm in enumerate(handsLms.landmark) :
          h, w, c = img.shape
          cx, cy = int (lm.x * w), int(lm.y * h)
          if (id == index) :
            if draw :
              cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
            res.append([cx, cy])
    return res

  def trackLandmarks(self, img, draw = True): # 跟踪所有坐标，默认在传入的图片上画出来，返回值是关键点的像素坐标
    res = []
    if self.__results.multi_hand_landmarks :
      for handsLms in self.__results.multi_hand_landmarks :
        for id, lm in enumerate(handsLms.landmark) :
          h, w, c = img.shape
          cx, cy = int (lm.x * w), int(lm.y * h)
          res.append([cx, cy])
          if draw :
            cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
    return res
  def _getLandmarks(self): # 返回识别的结果
    return self.__results.multi_hand_landmarks

# 躯体识别
class BodyDetector():
  def __init__(self):
    self.__mpDraw = mp.solutions.drawing_utils
    self.__mpStyles = mp.solutions.drawing_styles
    self.__mpPose = mp.solutions.pose
    self.__pose = self.__mpPose.Pose()
  def findBody(self, img, draw=True):
    image_height, image_width, _ = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    self.__results = self.__pose.process(imgRGB)
    if draw and self.__results.pose_landmarks:
      self.__mpDraw.draw_landmarks(
        img,
        self.__results.pose_landmarks,
        self.__mpPose.POSE_CONNECTIONS,
        landmark_drawing_spec=self.__mpStyles.get_default_pose_landmarks_style()
      )
  def trackLandmarks(self, img, draw = True): # 跟踪所有关键点坐标：头0、左肩12、右肩11、左腿24、右腿23, 右手手掌19
    res =  {}
    if self.__results.pose_landmarks :
      for id, lm in enumerate(self.__results.pose_landmarks.landmark) :
        if id in [0, 12, 11, 24, 23, 19]:
          id = Gesture(id)
          h, w, c = img.shape
          cx, cy = int (lm.x * w), int(lm.y * h)
          res[id] = (cx, cy)
          if draw :
            cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
    return res

class BodyController():
  def __init__(self):
    self.__bodyDetector = BodyDetector()
    self.__limit = 50
  def __help(self) -> Gesture:
    if self.__res != {}:
      hand = self.__res[Gesture.RIGHTHAND]
      for point in [Gesture.HEAD, Gesture.LEFTARM, Gesture.RIGHTARM, Gesture.LEFTLEG, Gesture.RIGHTLEG]:
        p = self.__res[point]
        if math.pow(math.pow(hand[0] - p[0], 2) + math.pow(hand[1] - p[1], 2), 0.5) < self.__limit:
          return point
      if hand[0] > self.__res[Gesture.LEFTARM][0] and hand[0] < self.__res[Gesture.RIGHTARM][0] and hand[1] > self.__res[Gesture.LEFTARM][1] and hand[1] < self.__res[Gesture.LEFTLEG][1]:
        return Gesture.BODY
    return Gesture.STANDBY
  def process(self, img) -> Gesture:
    self.__bodyDetector.findBody(img, True)
    self.__res = self.__bodyDetector.trackLandmarks(img, True)
    return self.__help()

if __name__ == '__main__':
  import sys
  sys.path.append('Gesture/core')
  from cv2_utils import Camera, waitKey, showImage, FPS
  camera = Camera()
  fps = FPS()
  body = BodyController()
  while True:
    img = camera.read()
    res = body.process(img)
    print(res)
    fps.printFps(img)
    showImage(img)
    if waitKey(1, 'q'):
      break
