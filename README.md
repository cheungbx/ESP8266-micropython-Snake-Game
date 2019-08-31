# ESP8266-micropython-Snake-Game
# A snake game written on ESP8266 micropython using I2C OLED SSD1306, buzzer and push buttons
# ----------------------------------------------------------
#  Snake Game Ported from gamebuino META circuit python to
#  ESP8266 (node MCU D1 mini)  micropython
# by Billy Cheung  2019 08 31
#
# ESP8266 game console GPIO pins layout
#
# I2C OLED SSD1306 
# GPIO4   D2---  SDA OLED
# GPIO5   D1---  SCL  OLED
#
# Speaker
# GPIO15  D8     Speaker
#
#buttons
# GPIO12  D6——  Left  
# GPIO13  D7——  Right      
# GPIO14  D5——  UP     
# GPIO2   D4——   Down    
# GPIO0   D3——   A
# =====================================
# Original notes from the author
#
# Gamebuino Academy Workshop
# https://gamebuino.com/academy/workshop/learn-to-code-a-snake-game-with-python
# ----------------------------------------------------------
# This game is based on the CircuitPython environment, which
# is an implementation of the Python language specific to
# microcontrollers. CircuitPython runs on the SAMD21G18
# architecture of the Gamebuino META.
# ----------------------------------------------------------
# Author: Steph
# Date: April 2019
# ----------------------------------------------------------
