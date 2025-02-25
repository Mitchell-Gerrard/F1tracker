import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import Data
import threading
import time
import matplotlib.pyplot as plt
import pandas as pd
Data=Data.Data('latest')
def updater():
   Data.Updater(buffer_lock)
def ploper():
  while True:
   try:
   # print('yo')
    with buffer_lock:
     ver=Data.cardata[Data.cardata.driver_number==1]
     print(ver['speed'].iloc[-1])
     #print(ver['date'].iloc[0])
    # print(ver['date'].iloc[-1])
     time.sleep(1)
   except:
     print('fail',Data.cardata['speed'])
     time.sleep(10)
cars=[4,1]
start,end=Data.laptimes(10,cars)
cardatas=Data.histcardata(start,end,cars)

nor=cardatas[cardatas['driver_number']==4]
ver=cardatas[cardatas['driver_number']==1]
plt.plot(pd.to_datetime(ver['date']),ver['speed'],label='ver')
plt.plot(pd.to_datetime(nor['date']),nor['speed'],label='nor')
plt.legend()
plt.show()
'''
buffer_lock = threading.Lock()
updatingthred=threading.Thread(target=updater)
updatingthred.start()

printing=threading.Thread(target=ploper)
printing.start()
'''