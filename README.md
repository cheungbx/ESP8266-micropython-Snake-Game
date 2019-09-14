## ----------------------------------------------------------
#  Snake.py Game for or I2C OLED,  Snakes.py for SPI OLED
#  ESP8266 (node MCU D1 mini)  micropython
# by Billy Cheung  2019 08 31
#
# ----------------------------------------------------------
# 
# ----------------------------------------------------------
# snake.py pin layout
# ----------------------------------------------------------
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
# ----------------------------------------------------------
# snakes.py pin layout
# ----------------------------------------------------------
# SPI OLED SSD1306 
# GND
# VCC
# D0/Sck - D5 (=GPIO14=HSCLK)
# D1/SDA - D7 (=GPIO13=HMOSI)
# RES    - D0 (=GPIO16)
# DC     - D4 (=GPIO2)
# CS     - D1 (=GPIO5)
# Speaker
# GPIO15  D8     Speaker
#
#buttons  A0
# A0 VCC-10K0-U-10K-L-10K-R-10K-D-10K-GND 
# GPIO0   D3——   A
