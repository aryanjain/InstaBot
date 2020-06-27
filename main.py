#from  tinderBot import TinderBot
from backup import TinderBot
from time import sleep
import math
import random
import time
from sqlConn import create_connection
import sqlConn
import sys

t_end = time.time() + ((60 * 60))

def looper():
    while time.time() <= t_end :
        try:
             
             bot.discover_posts()
        except Exception as e:
            print("in except")
            sleep(3)
            continue    
    print("While loop ends")

bot=TinderBot()
sleep(10)
bot.signIn()
output = looper()
