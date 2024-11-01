import pandas as pd
from datetime import datetime, timedelta
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import time as titi



response = urlopen(f'https://api.openf1.org/v1/car_data?session_key=latest&driver_number=4&date>2024-10-27T21:46:46.476000+00:00')
data = json.loads(response.read().decode('utf-8'))
cardata=pd.DataFrame(data)
print(cardata)
datehold=data[1]['date']
titi.sleep(10)
response = urlopen(f'https://api.openf1.org/v1/sessions?session_key=latest')
data = json.loads(response.read().decode('utf-8'))
Sessiondata=pd.DataFrame(data)
start=Sessiondata['date_start'][0]
print(Sessiondata)

print(start,datehold)