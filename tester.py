import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import Data
import threading
import time
data=Data.Data('latest')
def ploper():
    print(data.cardata['speed'])
updatingthred=threading.Thread(target=data.Updater)
updatingthred.start()
time.sleep(10)
printing=threading.Thread(target=ploper)
printing.start()
