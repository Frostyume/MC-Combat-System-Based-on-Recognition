'''
Author: linin00
Date: 2022-12-13 01:31:50
LastEditTime: 2022-12-13 23:03:17
LastEditors: linin00
Description: 
FilePath: /open/Gesture/src/user.py

'''
import sys
sys.path.append('./Gesture/core')
from game import PlayerController
from function import my_wearing, my_fighting
if __name__ == '__main__':
  name = input('input the player name: ')
  player = PlayerController(wearing = my_wearing, playername=name, fighting=my_fighting)
  player.start()
