'''
Author: linin00
Date: 2022-12-13 00:16:05
LastEditTime: 2022-12-14 17:23:53
LastEditors: linin00
Description: 
FilePath: /open/Gesture/core/game.py

'''
import sys
sys.path.append('./Gesture/core')
from mqtt_utils import Mqtt_async
sys.path.append('./Gesture/core/type')
import Topic, Msg
from mediapipe_utils import BodyController
from cv2_utils import Camera, waitKey, showImage, FPS
import time
sys.path.append("MC")
from function_MC import MC_Gameover
from function_MC import players as MC_Players

# 传入玩家列表和姿态信息，如果所有玩家都穿好了则返回真
def my_handleWearing(players: list, msg: str) -> bool:
  print('players', players, 'Wearing', msg)
  
  time.sleep(5) # 模拟玩家穿衣服的时间
  return True

# 传入玩家列表和招式信息，如果所有游戏结束则返回真
def my_handleFighting(players: dict, skill: str) -> bool:
  print('players', players, 'Skill', skill)
  print('winner', players)
  time.sleep(10) # 模拟玩家游戏的时间
  return True

class MCController():
  def __init__(self, handleWearing = my_handleWearing, handleFighting = my_handleFighting):
    print('hello, I am a MCController')
    self.mqtt = Mqtt_async('dev.linin.xyz', 8302)
    self.players = []
    self.maxPlayers = 4
    self.handleWearing = handleWearing
    self.handleFighting = handleFighting

  def waitingPlayers(self): # 通知玩家mc控制器准备就绪，并统计上线玩家数
    print('waiting for players...')
    self.mqtt.SUB(Topic.PLAYER)
    players = dict()
    while True: # 忙等待直到所有玩家就位
      name, topic = self.mqtt.getMsg()
      self.mqtt.PUB(Topic.MCCONTROLLER, Msg.MCCONTROLLER) # 发自己存在
      if topic == Topic.PLAYER and not (name in players.keys()): # 订阅到玩家登陆
        print(name, 'connected')
        players[name] = True # 记录一位玩家
        print('players amount:', len(players))
        if len(players) == self.maxPlayers: # 所有玩家到位，结束这个过程
          self.players = players.keys()
          self.mqtt.UNSUB(Topic.PLAYER)
          break

  def startWearing(self): # 开始游戏的第一阶段，穿盔甲
    print('wearing...')
    self.mqtt.SUB(Topic.POSE)
    while True:
      self.mqtt.PUB(Topic.GAMEBEGIN, Msg.GAMEBEGIN)
      msg, topic = self.mqtt.getMsg()
      if topic == Topic.POSE:
        res = self.handleWearing(self.players, msg) # 处理穿衣服的函数，如果所有人都穿好了就退出
        if res == True:
          break
    self.mqtt.UNSUB(Topic.POSE) # 取消订阅

  def startFighting(self): # 对局开始，打斗控制
    print('fighting...')
    self.mqtt.SUB(Topic.SKILL) # 订阅不同人发出的技能
    while True:
      self.mqtt.PUB(Topic.ALLREADY, Msg.ALLREADY) # 通知：大家都穿好了
      skill, topic = self.mqtt.getMsg()
      res = False
      if topic == Topic.SKILL:
        res = self.handleFighting(self.players, skill) # 处理玩家技能技能，如果游戏结束返回真
      res = res or MC_Gameover(MC_Players.get("Global")) # 避免玩家不发技能时无法接受到退出游戏的消息
      if res == True:
        break
    self.mqtt.UNSUB(Topic.SKILL) # 取消订阅

  def gameOver(self): # 游戏结束，输出结果
    self.mqtt.PUB(Topic.GAMEOVER, Msg.GAMEOVER) # 通知：游戏结束
    print('gameOver')
    time.sleep(1)
    self.mqtt.PUB(Topic.GAMEOVER, Msg.GAMEOVER) # 再次通知：游戏结束
  
  def start(self):
    print('controller started')
    self.waitingPlayers()
    self.startWearing()
    self.startFighting()
    self.gameOver()



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
    elif res == Gesture.LeftARM:
      mqtt.PUB(Topic.POSE, prefix + Msg.LeftARM)  # 左臂
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
  cv2.destroyAllWindows() # 关闭窗口

def my_fighting(mqtt: Mqtt_async, prefix: str):
  print('fighting demo...')
  mqtt.PUB(Topic.SKILL, Msg.DEMO)

class PlayerController():
  def __init__(self, playername='DemoPlayer', wearing=my_wearing, fighting=my_fighting):
    self.playername = playername
    self.mqtt = Mqtt_async('dev.linin.xyz', 8302)
    self.bodyController = BodyController
    self.prefix = self.playername+':'

    self.__wearingImpl = wearing
    self.__fightingImpl = fighting
    print('hello', self.playername)
  def __check_mcController(self):
    print('Checking mc controller...')
    self.mqtt.SUB(Topic.MCCONTROLLER)
    while True:
      self.mqtt.PUB(Topic.PLAYER, self.playername) # 通知mc我已上线
      msg, topic = self.mqtt.getMsg()
      if topic == Topic.MCCONTROLLER and msg == Msg.MCCONTROLLER: 
        print('mcController exists')
        # self.mqtt.UNSUB(Topic.MCCONTROLLER) # 不再订阅这条消息
        break

  def __preparing(self):
    print('Waiting for other players...')
    self.mqtt.SUB(Topic.GAMEBEGIN)
    while True: # 忙等待直到游戏开始
      msg, topic = self.mqtt.getMsg()
      if topic == Topic.GAMEBEGIN and msg == Msg.GAMEBEGIN:
        print('all players are ready to go')
        self.mqtt.UNSUB(Topic.GAMEBEGIN) # 不再订阅
        break

  def __wearing(self):
    print('The player is wearing armor...')
    self.__wearingImpl(self.bodyController, self.mqtt, self.prefix) # 执行穿盔甲任务
    print('all players are ready to fight')

  def __fighting(self):
    print('Game on, enjoy the fight, warrior!!')
    self.__fightingImpl(prefix=self.prefix, mqtt=self.mqtt) # 执行声音控制指令

  def __gameOver(self):
    print('Game over')

  def start(self):
    print('game started, welcome', self.playername)
    # 等待mcController上线
    self.__check_mcController()
    # 等待通知游戏开始
    self.__preparing()
    # 穿衣服
    self.__wearing()
    # 游戏开始
    self.__fighting()
    # 游戏结束
    self.__gameOver()


if __name__ == '__main__':
  player = PlayerController()
  player.start()