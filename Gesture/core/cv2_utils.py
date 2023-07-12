'''
Author: linin00
Date: 2022-12-07 18:40:29
LastEditTime: 2022-12-13 03:15:23
LastEditors: linin00
Description: 
FilePath: /open/Gesture/core/cv2_utils.py

'''

import cv2
import time

# 显示帧率
class FPS:
  def __init__(self):
    super()
    self.__ctime = 0
    self.__ptime = 0
    self.__fps = 0
  def __titok(self):
    self.__ctime = time.time()
    self.__fps = 1 / (self.__ctime - self.__ptime)
    self.__ptime = self.__ctime
  def printFps(self, img):
    self.__titok()
    cv2.putText(img, str(int(self.__fps)), (10, 70), 
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

# 读取摄像头图片
class Camera:
  def __init__(self, idx = 0):
    super()
    self.__cap = cv2.VideoCapture(idx)
  def read(self, flip = True): # 默认使用笔记本前置摄像头，需要照y轴做镜像反转
    success, img = self.__cap.read()
    if flip :
      img = cv2.flip(img, 1)
    return img

# 在time毫秒内等待一个按键输入
def waitKey(time, key):
  return cv2.waitKey(time) & 0xff == ord(key)

# 显示图片
def showImage(img, name='image') :
  cv2.imshow(name, img)

def destroy():
  cv2.destroyAllWindows() # 关闭窗口