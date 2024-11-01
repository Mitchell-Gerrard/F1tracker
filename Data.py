import pandas as pd
from datetime import datetime, timedelta
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import time
class Data:

  def __init__(self,Session):
    ''' Either ask question opening a dialog box this varable will be changeable ill think how soon'''
    self.Session=Session
    self.Freq=1
    response = urlopen(f'https://api.openf1.org/v1/sessions?session_key={self.Session}')
    data = json.loads(response.read().decode('utf-8'))
    self.Sessiondata=pd.DataFrame(data)
    
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
    QUERY_FREQUENCY = 3  # Query data every 3 seconds
    DELAY = 10 
    last_query_time = datetime.now() - timedelta(seconds=DELAY)
    while True:
        try:
            # Format the timestamp for the API call
            formatted_time = last_query_time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
            url = f"https://api.openf1.org/v1/car_data?session_key=latest&date>{formatted_time}"
            response = urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
            
            cardata=pd.DataFrame(data)

            with buffer_lock:
                self.cardata = pd.concat([self.cardata,cardata])
                # Add new data to the buffer
                
            # Update last_query_time to the time of the last data point received
            if data:
                last_query_time = datetime.strptime(data[-1]['date'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
            
            time.sleep(QUERY_FREQUENCY)  # Wait for a few seconds before next API call
        except Exception as e:
            print(f"Error fetching speed data: {e}")
            time.sleep(QUERY_FREQUENCY)  # In case of an error, wait before trying again
  def histcardata(self,B_times,E_times,cars):
    notdone=True
    cardata=1
    while notdone:
      try:
            for i, car in enumerate(cars):
              # Format the timestamp for the API call
              B_time=B_times[i]
              E_time=E_times[i]
              print(B_time,E_time)
              B_timeF = B_time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
              E_timeF = E_time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
              url = f"https://api.openf1.org/v1/car_data?driver_number={car}&session_key={self.Session}&date>={B_timeF}&date<={E_timeF}"
              response = urlopen(url)
              data = json.loads(response.read().decode('utf-8'))
              
              if  isinstance(cardata, pd.DataFrame):
                 data=pd.DataFrame(data)
                 cardata=pd.concat([cardata,data])
              else:
                 cardata=pd.DataFrame(data)

                  # Add new data to the buffer
                  
              # Update last_query_time to the time of the last data point received
              notdone=False
            return(cardata)
              # Wait for a few seconds before next API call
      except Exception as e:
              print(f"Error fetching speed data: {e}")
              time.sleep(10)  # In case of an error, wait before trying again
  def laptimes(self,lap,cars):
      B_times=[]
      E_times=[]
      for car in cars:
              url = f"https://api.openf1.org/v1/laps?driver_number={car}&session_key={self.Session}&lap_number={lap}"
              response = urlopen(url)
              data = json.loads(response.read().decode('utf-8'))
              laps=pd.DataFrame(data)
              B_time=laps['date_start'][0]
              B_time=datetime.strptime(B_time, '%Y-%m-%dT%H:%M:%S.%f+00:00')
              lap_time=laps['lap_duration'][0]
              E_time=B_time+timedelta(seconds=lap_time)
              B_times.append(B_time)
              E_times.append(E_time)
              time.sleep(1)
      return(B_times,E_times)

