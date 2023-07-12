'''
Author: linin00
Date: 2022-12-13 01:31:57
LastEditTime: 2022-12-13 01:38:44
LastEditors: linin00
Description: 
FilePath: /open/Gesture/src/controller.py

'''
import sys
sys.path.append('./Gesture/core')
from game import MCController
sys.path.append("./MC")
from function_MC import my_handleWearing, my_handleFighting

if __name__ == '__main__':
  mc = MCController(handleWearing = my_handleWearing, handleFighting = my_handleFighting)
  mc.start()