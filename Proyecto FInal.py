import tkinter as tk
from tkinter import filedialog
import sys


class Process:
    def __init__(self, pid, arrtime, cputime, timerem, timeexit, priority, io):
        self.pid = pid
        self.arrtime = arrtime
        self.cputime = cputime
        self.timerem = timerem
        self.timeexit = timeexit
        self.priority = priority
        self.io = io


def run_schedule():
    print()
    cpus = []
    for x in range(0, cpunumber):
        cpus.append("EMPTY")
    while any (p.timerem > 0 for p in processlist):
        for i in range(0, cpunumber):
           if cpu[i] == "EMPTY":
               cpu[i] = 0


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
f = open(file_path, "r")
with f as file:
    lines = file.readlines()

lines = [x.strip() for x in lines]

if lines[0] == "PrioPreentive" or lines[0] == "PrioNotPreentive":
    politica = lines[0]
else:
    sys.exit()
print("IM HERE")
print(lines[0])
w1,w2 = lines[1].split(" ")
print(isinstance(int(w2), int))

if w1 == "QUANTUM" and isinstance(int(w2), int):
    quantum = int(w2)
else:
    sys.exit()
print("IM HERE")
print(w1,w2)
w1, w2, w3 = lines[2].split(" ")
print (isinstance(w3, int))
if w1 == "CONTEXT" and w2 == "SWITCH" and isinstance(int(w3), int):
    contextswitch = int(w3)
else:
    sys.exit()
print("IM HERE")
print(w1,w2,w3)
w1, w2 = lines[3].split(" ")

if w1 == "CPUS" and isinstance(int(w2), int):
    cpunumber = int(w2)
else:
    sys.exit()
print("IM HERE")
print(w1,w2)
processlist = []

for iter in range(4, len(lines)):
    iodictionary = {}
    if lines[iter] == "FIN":
        break
    else:
        w = lines[iter].split(" ")
        print(w)
        w0 = w[0]
        print(w0)
        w1 = w[1]
        w2 = w[2]
        w3 = w[3]
        if isinstance(int(w0), int) and isinstance(int(w1), int) and isinstance(int(w2), int) and isinstance(int(w3), int):
            if len(w) > 4 and w[4] == "I/O":
                for i in range(5, len(w)-1):
                    wi = w[i]
                    wi1 = w[i+1]
                    if isinstance(int(wi), int) and isinstance(int(wi1), int):
                        iodictionary[int(wi)] = int(wi1)
                        i = i+1
                    else:
                        sys.exit()
        else:
            sys.exit()
        process = Process(int(w0), int(w1), int(w2), int(w2), 0, int(w3), iodictionary)
        processlist.append(process)

run_schedule()
            
