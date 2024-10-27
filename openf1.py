from urllib.request import urlopen
import json
import pandas as pd
import matplotlib.pyplot as plt
response = urlopen('https://api.openf1.org/v1/intervals?session_key=9159')
data = json.loads(response.read().decode('utf-8'))
df=pd.DataFrame(data)
print(df.head())
print(df.columns)

