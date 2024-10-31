import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import Data
import threading
import time
data=Data.Data('9159')
def updater():
   data.Updater(buffer_lock)
def ploper():
  while True:
   try:
   # print('yo')
    with buffer_lock:
     ver=data.cardata[data.cardata.driver_number==1]
     print(ver['speed'].iloc[-1])
     #print(ver['date'].iloc[0])
    # print(ver['date'].iloc[-1])
     time.sleep(1)
   except:
     print('fail',data.cardata['speed'])
     time.sleep(10)
buffer_lock = threading.Lock()
updatingthred=threading.Thread(target=updater)
updatingthred.start()

printing=threading.Thread(target=ploper)
printing.start()
