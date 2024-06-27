# -*- coding: utf-8 -*-
'''
PWM frequency higher than 2K, there may be relatively large difference between the frequency and the set value. 
For frequency higher than 2K, please refer to the following frequency value: 
46875HZ, 23437HZ, 15625HZ, 11718HZ,
9375HZ, 7812HZ, 6696HZ, 5859HZ, 5208HZ, 4687HZ, 4261HZ,
3906HZ, 3605HZ, 3348HZ, 3125HZ,
2929HZ, 2757HZ, 2604HZ, 2467HZ, 2343HZ, 2232HZ, 2130HZ, 2038HZ,
'''

import time
from pinpong.board import Board
from pinpong.libs.dfrobot_dri0050 import DRI0050 # Import DRI0050 library from libs 

def turn_on():
  # #Board("RPi").begin()  #RPi Linux platform 
  # Board("Win").begin() #windows platform

  # #pwmd = DRI0050(port="/dev/ttyUSB0") #RPi Linux platform
  # pwmd = DRI0050(port="COM5")  #Windows platform

  # print("version=0x{:x}, addr=0x{:x}".format(pwmd.get_version(), pwmd.get_addr()))
  # print("pid=0x{:x}, vid=0x{:x}".format(pwmd.get_vid(), pwmd.get_pid()))

  # while True:
  #   print("\n--------Inital Value------") 
  #   print("freq={}, duty={:.2f} enable={}".format(pwmd.get_freq(), pwmd.get_duty(), pwmd.get_enable()))  

  #   print("--------Set a new value------")  
  #   #pwmd.pwm(freq=860,duty=0.82) # freq(183HZ-46875HZ) duty(0%-100%)
  #   pwmd.set_freq(860) #(183HZ-46875HZ)
  #   pwmd.set_duty(0.82)#(0%-100%)
  #   pwmd.set_enable(1)
  #   print("freq={}, duty={:.2f} enable={}".format(pwmd.get_freq(), pwmd.get_duty(), pwmd.get_enable()))

  #   print("--------Restore to factory settings (366HZ, duty ratio 50%, disable output)-------\n")
  #   pwmd.pwm(freq=366,duty=0.5) # freq(183HZ-46875HZ) duty(0%-100%)
  #   pwmd.set_enable(0)
  #   time.sleep(5)
    
  # second format
  
  Board("Win").begin() #windows platform
  
  pwmd = DRI0050(port="COM5")  #Windows platform
  
  pwmres = 0.1
  pwnD = 0
  
  while True:
    pwmres = 0.1
    pwmD = 0
    
    for i in range (0,10):
      pwmd.set_freq(1000)
      pwmD = pwmD + pwmres
      pwmd.set_duty(pwmD)
      
      pwmd.set_freq(1)
      time.sleep(0.5)
      
    for i in range(0, 10):
      pwmd.set_freq(1000)
      pwmD = pwmD - pwmres
      pwmd.set_duty(pwmD)
      
      pwmd.set_freq(1)
      time.sleep(0.5)
  
  pwmd.set_enable(0)
  time.sleep(0.5)