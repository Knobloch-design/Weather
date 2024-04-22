import requests
import pandas as pd
import json
from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta


"""

SO Im thinking about creating a linked list type data structure that connects days together

a day object needs to store:
    - pointer to day before it
    - pointer to day after it 
    - sunrise
    - sunset
    - max temp
    - min temp
    - visibility forecast

maybe this could also include hourly information with the same concept of pointing to hours before and after it

an hour object needs to store:
    - temp
    - dewpoint
    - relative humidity
    - apparent temp
    - skycover
    - windspeed
    - wind gust speed
    - hourly mixing height
    - probability of percipition 




"""

class dayWeather:

    
    def __init__(self, date, sunrise, sunset, maxtemp, mintemp, visibility, prev = None, next = None):
        self.date = date
        self.sunrise = sunrise
        self.sunset = sunset
        self.maxtemp = maxtemp
        self.mintemp = mintemp
        self.visibility = visibility
        if prev != None:
            prev.set_next_hr(self)
            self.prev = prev
        else:
            self.prev = prev 
        self.next = next
        
    def set_next_day(self, next_day):
        self.next = next_day
        
    def get_next_day(self):
        return self.next

    def set_prev_day(self, prev_day):
        self.prev = prev_day
        
    def get_prev_day(self):
        return self.prev
    





class hourWeather:

    def __init__(self, timeStart = None,tempForecast = None,dewPointForecast = None,relativeHumidityForecast = None, skyCoverForecast = None, windSpeedForecast = None, prev = None, next = None):
        self.timeStart = timeStart
        self.tempForecast = tempForecast
        self.dewPointForecast = dewPointForecast
        self.relativeHumidityForecast = relativeHumidityForecast
        self.skyCoverForecast = skyCoverForecast
        self.windSpeedForecast = windSpeedForecast

        if prev != None:
            prev.set_next_hr(self)
            self.prev = prev
        else:
            self.prev = prev 
        self.next = next
        

    def set_next_hr(self, next_hr):
        self.next = next_hr
        
    def get_next_hr(self):
        return self.next

    def set_prev_hr(self, prev_hr):
        self.prev = prev_hr
        
    def get_prev_hr(self):
        return self.prev
    
    def insertNext(self, Node):
        self.next.prev = Node
        Node.next = self.next
        Node.prev = self
        self.next = Node

    def getHead(self):

        if self.prev == None:
            print("got here")
            print(type(self))

            return self
        else:
            print(self.tempForecast)
            return self.prev.getHead()
            


"""
test1 = hourWeather(1,1,1,1,1,1)
test3 = hourWeather(3,3,3,3,3,3,test1)
test2 = hourWeather(2,2,2,2,2,2)

test1.insertNext(test2)
print(test1.tempForecast)
print(test2.tempForecast)
print(test3.tempForecast)

print(type(test3.getHead()))
#print(node.tempForecast)
"""
