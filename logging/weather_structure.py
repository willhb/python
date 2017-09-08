#!/usr/bin/env python

import time
import socket
import requests
import json
import subprocess


class WeatherData :

    def __eq__(self,other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__dict__ == other.__dict__
    
    mWeatherData = { 'time'     : 0 ,
                     'model'    : 0 ,
                     'sensor_id': 0 ,
                     'channel'  : 0 ,
                     'humidity' : 0 ,
                     'temp'     : 0 ,
                     'tempF'    : 0 } 
        
class WeatherParse :
    """
    
    """
    def __init__(self):
        """
        Constructor 
        """
        self.mSavedData = [WeatherData for _ in range(3)]
        self.mToSend    = WeatherData()
        
        self.mNumSaved         = 0
        self.mLastSentTime     = 0
        self.mCurrentSavedTime = 0
        self.mCurrentFrameTime = 0
        self.mSend             = False
        self.mDataLine         = ""
        
        self.mProc = subprocess.Popen( ['rtl_433','-Fjson','-q','-R 40'],
                                       stdout=subprocess.PIPE)

    def run(self):
        while True:
            try:
                self.mDataLine = self.mProc.stdout.readline()

                self.processData(self.mDataLine)
                
                if self.mSend :
                    self.sendData()
                
                
            except BaseException as e:
                print "Exception: %s" % (str(e))
                return 


    def vote(self):

        if ( self.mSavedData[0] == self.mSavedData[1] ) or ( self.mSavedData[0] == self.mSavedData[2] ):            
            self.mToSend.mWeatherData = self.mSavedData[0].mWeatherData
        elif self.mSavedData[1] == self.mSavedData[2] :
            self.mToSend.mWeatherData = self.mSavedData[1].mWeatherData
        else :
            print "No data agrees, skip"
            self.mSend = False            
            
    def processData(self, dataLine ):
        
        if dataLine[0] == "{":
            line  = json.loads(dataLine)
            model = line[u'model']
            time  = line[u'time']

            self.mCurrentFrameTime = time
            
            # THis part is not right
            if model == "Acurite tower sensor":
                    
                if ( self.mCurrentFrameTime != self.mCurrentSavedTime ) and ( self.mNumSaved <> 0):
                    print "New Set %s vs %s" % ( self.mCurrentFrameTime, self.mCurrentSavedTime)
                    
                    self.vote()
                    self.mCurrentSavedTime = self.mCurrentFrameTime
                    self.mSend = True
                    self.mNumSaved = 0

                self.mSavedData[self.mNumSaved].mWeatherData['sensor_id'] = line[u'id']
                self.mSavedData[self.mNumSaved].mWeatherData['channel']   = line[u'channel']
                self.mSavedData[self.mNumSaved].mWeatherData['humidity']  = line[u'humidity']
                self.mSavedData[self.mNumSaved].mWeatherData['tempF']     = (line[u'temperature_C'] * (9.0/5.0))+32
                self.mSavedData[self.mNumSaved].mWeatherData['time']      = time
                self.mSavedData[self.mNumSaved].mWeatherData['model']     = model

                # Update our current saved time
                self.mCurrentSavedTime = self.mCurrentFrameTime
                self.mNumSaved += 1                

                if self.mNumSaved >= 3:
                    self.mSend = True
                    self.mNumSaved = 0 
                    self.mCurrentSavedTime = 0
                                                      
    def sendData(self):
        try:
            #sendString = 'temp_'+str(channel)+',host=viatiempo temperature='+str(tempF)+',humidity='+str(humidity)+',battery='+str(battery)
            sendString = ( "temp_%s,host=rpi4 temperature=%s,humidity=%s,battery=0" %
                           ( self.mToSend.mWeatherData['channel'], self.mToSend.mWeatherData['tempF'],
                             self.mToSend.mWeatherData['humidity'] )
                           )
            
            res = requests.post(url='http://192.168.2.32:8186/write', data=sendString)

            print("Posted: %s" % sendString)
            
        except BaseException as e:
            print "Could not post: Exception: %s" % (str(e))

        self.mSend     = False
        self.mNumSaved = 0
        

                                                      
                
            
def main():
    print "Main Thread"
    weather_parser = WeatherParse()
    weather_parser.run()


if __name__ == '__main__':
    main()


