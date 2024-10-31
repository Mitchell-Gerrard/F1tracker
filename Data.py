import pandas as pd
from datetime import datetime, timedelta
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import time as titi
class Data:

  def __init__(self,Session):
    ''' Either ask question opening a dialog box this varable will be changeable ill think how soon'''
    self.Session=Session
    self.Freq=1
    response = urlopen(f'https://api.openf1.org/v1/sessions?session_key={self.Session}')
    data = json.loads(response.read().decode('utf-8'))
    self.Sessiondata=pd.DataFrame(data)
    print(self.Sessiondata.columns)
    print(self.Sessiondata)
    self.start=self.Sessiondata['date_start'][0]
    print('start',self.start)
    response = urlopen(f'https://api.openf1.org/v1/car_data?session_key={Session}&driver_number=4')
    data = json.loads(response.read().decode('utf-8'))
    cardata=pd.DataFrame(data)
    self.cardata = pd.DataFrame(columns=cardata.columns)
    print('firstdata', cardata['date'][1])
    self.firsttime = cardata['date'][1]
    print(self.firsttime)
    #formatted_time = last_query_time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
    print(self.cardata.columns,cardata.columns,cardata)
    '''
    titi.sleep(1)
    response = urlopen(f'https://api.openf1.org/v1/intervals?session_key={self.Session}&{self.start}')
    data = json.loads(response.read().decode('utf-8'))
    print(self.cardata)
    intervaldata=pd.DataFrame(data)
    self.intervaldata=pd.DataFrame(columns=intervaldata.columns)
    '''
  def Updater(self,buffer_lock):
      # Correct format without milliseconds

    last_query_time = datetime.strptime(self.firsttime, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    time=self.start
    print('yo')
    while True:
     try:
      formatted_time = last_query_time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
      print(formatted_time)
      response = urlopen(f'https://api.openf1.org/v1/car_data?session_key={self.Session}&date<{formatted_time}')
      data = json.loads(response.read().decode('utf-8'))
      cardata=pd.DataFrame(data)
      with buffer_lock:
       self.cardata = pd.concat([self.cardata,cardata])
      titi.sleep(int(self.Freq))
      print('up',last_query_time,len(cardata))
      last_query_time = datetime.strptime(data[-1]['date'], '%Y-%m-%dT%H:%M:%S.%f+00:00')+ timedelta(seconds=30)
      print(last_query_time,data[-1]['date'],data[0]['date'])
     except Exception as e:
       print(e)
       titi.sleep(int(self.Freq))
     '''

     response = urlopen(f'https://api.openf1.org/v1/intervals?session_key={self.Session}&{formatted_time}')
     data = json.loads(response.read().decode('utf-8'))
     intervaldata=pd.DataFrame(data)
     self.intervaldata = pd.concat(self.intervaldata,intervaldata)
    '''
