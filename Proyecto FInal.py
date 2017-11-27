import tkinter as tk
from tkinter import filedialog
import sys
import time

class Process:
    def __init__(self, pid, proccid, arrtime, cputime, timerem, timeexit, priority, io):
        self.pid = pid
        self.proccid = proccid
        self.arrtime = arrtime
        self.cputime = cputime
        self.timerem = timerem
        self.timeexit = timeexit
        self.priority = priority
        self.io = io

    def __repr__(self):
        return str(self.pid) + " " + str(self.arrtime) + " " + str(self.cputime) + " " + str(self.timerem) \
        + " " + str(self.timeexit) + " " + str(self.priority)

#Validación si existe un proceso con mayor prioridad
def validate_prio(p):
    global readyqueue
    flag = False
    for x in readyqueue:
        if x.priority > p.priority:
            flag = True
            break
        elif x.priority == p.priority and x.arrtime < p.arrtime:
            flag = True
            break
    return flag

#Variables globales de promedios para comparar al final
waitavg = 0
turnar = 0

#No Expropiativo
def run_schedule_nonpreempt():
    print("========================NONPREEMPTIVE==========================")
    global readyqueue
    #Listas y filas
    cpus = []
    readyqueue = []
    blockedqueue = []
    blockedfor = []
    #Contador de tiempo
    timer = 0
    #Inicializar cpus en vacio
    for x in range(0, cpunumber):
        cpus.append("EMPTY")
    #ciclo de simulación
    while True:
        #Ciclo para actualizar valores en ejecución
        for i in range(0, cpunumber):
            if cpus[i] != "EMPTY":
                #Actualizar el tiempo restante de cpu
                cpus[i].timerem = cpus[i].timerem - 1

                #Si ya acabo de ejecutarse, salirse del cpu y actualizar tiempo de salida
                if cpus[i].timerem == 0:
                    for p in processlist:
                        if cpus[i].pid == p.pid:
                            p.timeexit = timer
                    cpus[i] = "EMPTY"
                
                else:
                    timeio = cpus[i].cputime - cpus[i].timerem
                    #Si hay un tiempo de I/O pasar proceso a cola de bloqueados y desalojar cpu
                    if timeio in cpus[i].io:
                        blockedfor.append(cpus[i].io[timeio])
                        blockedqueue.append(cpus[i])
                        cpus[i] = "EMPTY"
        #Si el tiempo coincide con el tiempo de llegada de un procesom agregarlo a la cola de listos           
        for p in processlist:
            if timer == p.arrtime:
                readyqueue.append(p)
                
        #Si la operación de I/O ha finalizado, meter el proceso a la cola de listos
        for p in range(0, len(blockedqueue)):
            if blockedfor[p] == 0:
                readyqueue.append(blockedqueue[p])
                blockedqueue.remove(blockedqueue[p])
                blockedfor.remove(blockedfor[p])
                
        #Si hay un cpu vacio
        if any(c == "EMPTY" for c in cpus):
            for i in range(0, cpunumber):
                for p in readyqueue:
                    #Si no existe un proceso con mayor prioridad en la pila de listos y el cpu iterado esta vacio
                    #meterlo en ese cpu y sacarlo de la cola de listos
                    if not validate_prio(p) and cpus[i] == "EMPTY":
                        timer += contextswitch
                        cpus[i] = p
                        readyqueue.remove(p)
        #Impresión de datos
        for c in range(0,cpunumber):
            print("CPU ", c+1)
            print()
            print("TIEMPO")
            print(timer)
            print()
            print("LISTOS")
            for r in readyqueue:
                print(r.proccid, "(", r.timerem,")",end=" ")
            print()
            print("CPU")
            if cpus[c] == "EMPTY":
                print(cpus[c])
            else:
                print(cpus[c].proccid, "(", cpus[c].timerem, ")")
            print()
            print("BLOQUEADOS")
            for blocked in blockedqueue:
                print(blocked.proccid, end=" ")
            print()
            print("=============================")
            
        #Actualización del timer
        timer += 1

        #Actualización de timers de operacioes I/O
        for b in range(0, len(blockedfor)):
            blockedfor[b] -= 1

        #Si ya no quedan procesos por ejecutar, salir del ciclo
        if not any(p.timeexit == 0 for p in processlist):
            break
    #Inicialización de listas para datos
    waitingtime = []
    turnaround = []
    print("========================NONPREEMPTIVE==========================")
    for p in range(0, len(processlist)):
        #Calcular Turnaround = Tiempo de salida - tiempo de llegada
        turnaround.append(processlist[p].timeexit - processlist[p].arrtime)
        #Calcular Tiempo de espera = Turnaround - tiempo de cpu
        waitingtime.append(turnaround[p] - processlist[p].cputime)
        print(processlist[p].proccid, " T.ESPERA: ", waitingtime[p], " TURNAROUND: ", turnaround[p])
        print()
    acum1 = 0
    acum2 = 0
    #Obtener promedios
    for t in range(0, len(turnaround)):
        acum1 += turnaround[t]
        acum2 += waitingtime[t]

    global waitavg
    global turnar
    waitavg = float(acum2/len(processlist))
    turnar = float(acum1/len(processlist))
    print("T.ESPERA PROMEDIO: ", waitavg)
    print()
    print("TURNAROUND PROMEDIO: ", turnar)

def get_max_prio():
    global readyqueue
    acum = readyqueue[0]
    for p in reversed(readyqueue):
        if p.priority > acum.priority:
            acum = p
    return acum

#Variables globales de promedios para comparar al final
waitavg2 = 0
turnar2 = 0

#Expropiativo
def run_schedule_preempt():
    global readyqueue
    #Listas y filas
    print("========================PREEMPTIVE==========================")
    cpus = []
    readyqueue = []
    blockedqueue = []
    blockedfor = []
    #Contador de tiempo
    timer = 0
    #Inicializar cpus en vacio
    for x in range(0, cpunumber):
        cpus.append("EMPTY")
    #ciclo de simulación
    while True:
        #Ciclo para actualizar valores en ejecución
        for i in range(0, cpunumber):
            if cpus[i] != "EMPTY":
                #Actualizar el tiempo restante de cpu
                cpus[i].timerem = cpus[i].timerem - 1

                #Si ya acabo de ejecutarse, salirse del cpu y actualizar tiempo de salida
                if cpus[i].timerem == 0:
                    for p in processlistb:
                        if cpus[i].pid == p.pid:
                            p.timeexit = timer
                    cpus[i] = "EMPTY"
                
                else:
                    timeio = cpus[i].cputime - cpus[i].timerem
                    #Si hay un tiempo de I/O pasar proceso a cola de bloqueados y desalojar cpu
                    if timeio in cpus[i].io:
                        blockedfor.append(cpus[i].io[timeio])
                        blockedqueue.append(cpus[i])
                        cpus[i] = "EMPTY"
        #Si el tiempo coincide con el tiempo de llegada de un procesom agregarlo a la cola de listos           
        for p in processlistb:
            if timer == p.arrtime:
                readyqueue.append(p)
                
        #Si la operación de I/O ha finalizado, meter el proceso a la cola de listos
        for p in range(0, len(blockedqueue)):
            if blockedfor[p] == 0:
                readyqueue.append(blockedqueue[p])
                blockedqueue.remove(blockedqueue[p])
                blockedfor.remove(blockedfor[p])
                
        #Si hay un cpu vacio
        if any(c == "EMPTY" for c in cpus):
            for i in range(0, cpunumber):
                for p in readyqueue:
                    #Si no existe un proceso con mayor prioridad en la pila de listos y el cpu iterado esta vacio
                    #meterlo en ese cpu y sacarlo de la cola de listos
                    if not validate_prio(p) and cpus[i] == "EMPTY":
                        timer += contextswitch
                        cpus[i] = p
                        readyqueue.remove(p)
        #Si los cpus tienen procesos en ejecución
        else:
            for i in range(0, cpunumber):
                #Si hay procesos con mayor prioridad en la cola de listos
                if validate_prio(cpus[i]):
                    #Regresar a la cola de listos el proceso actual
                    readyqueue.append(cpus[i])
                    #Obtener el proceso con mayor prioridad y ponerlo en el cpu
                    cpus[i] = get_max_prio()
                    #Quitar el procesos de la cola de listos
                    readyqueue.remove(cpus[i])
                    
        #Impresión de datos
        for c in range(0,cpunumber):
            print("CPU ", c+1)
            print()
            print("TIEMPO")
            print(timer)
            print()
            print("LISTOS")
            for r in readyqueue:
                print(r.proccid, "(", r.timerem,")",end=" ")
            print()
            print("CPU")
            if cpus[c] == "EMPTY":
                print(cpus[c])
            else:
                print(cpus[c].proccid, "(", cpus[c].timerem, ")")
            print()
            print("BLOQUEADOS")
            for blocked in blockedqueue:
                print(blocked.proccid, end=" ")
            print()
            print("=============================")
            
        #Actualización del timer
        timer += 1

        #Actualización de timers de operacioes I/O
        for b in range(0, len(blockedfor)):
            blockedfor[b] -= 1

        #Si ya no quedan procesos por ejecutar, salir del ciclo
        if not any(p.timeexit == 0 for p in processlistb):
            break
    #Inicialización de listas para datos
    waitingtime = []
    turnaround = []
    
    for p in range(0, len(processlistb)):
        #Calcular Turnaround = Tiempo de salida - tiempo de llegada
        turnaround.append(processlistb[p].timeexit - processlistb[p].arrtime)
        #Calcular Tiempo de espera = Turnaround - tiempo de cpu
        waitingtime.append(turnaround[p] - processlistb[p].cputime)
        print(processlistb[p].proccid, " T.ESPERA: ", waitingtime[p], " TURNAROUND: ", turnaround[p])
        print()
    acum1 = 0
    acum2 = 0
    #Obtener promedios
    for t in range(0, len(turnaround)):
        acum1 += turnaround[t]
        acum2 += waitingtime[t]

    global waitavg2
    global turnar2
    print("========================PREEMPTIVE==========================")
    waitavg2 = float(acum2/len(processlist))
    turnar2 = float(acum1/len(processlist))
    print("T.ESPERA PROMEDIO: ", waitavg2)
    print()
    print("TURNAROUND PROMEDIO: ", turnar2)

    
    
        


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
    print("DATOS NO VALIDOS")
    sys.exit()

w1,w2 = lines[1].split(" ")

if w1 == "QUANTUM" and isinstance(int(w2), int):
    quantum = int(w2)
else:
    print("DATOS NO VALIDOS")
    sys.exit()

w1, w2, w3 = lines[2].split(" ")

if w1 == "CONTEXT" and w2 == "SWITCH" and isinstance(int(w3), int):
    contextswitch = int(w3)
else:
    print("DATOS NO VALIDOS")
    sys.exit()

w1, w2 = lines[3].split(" ")

if w1 == "CPUS" and isinstance(int(w2), int):
    cpunumber = int(w2)
else:
    print("DATOS NO VALIDOS")
    sys.exit()

processlist = []
processlistb = []
iterador = 0
for iter in range(4, len(lines)):
    iodictionary = {}
    if lines[iter] == "FIN":
        break
    else:
        w = lines[iter].split(" ")
        w0 = w[0]
        w1 = w[1]
        w2 = w[2]
        w3 = w[3]
        if isinstance(int(w0), int) and isinstance(int(w1), int) and isinstance(int(w2), int):
            if w[3] == "PRIORITY":
                w4 = w[4]
                if len(w) > 5 and w[5] == "I/O":
                    for i in range(6, len(w)-1):
                        if i % 2 == 0:
                            wi = w[i]
                            wi1 = w[i+1]
                            if isinstance(int(wi), int) and isinstance(int(wi1), int):
                                iodictionary[int(wi)] = int(wi1)
                            else:
                                print("DATOS NO VALIDOS")
                                sys.exit()
        else:
            print("DATOS NO VALIDOS")
            sys.exit()
        process = Process(iterador, int(w0), int(w1), int(w2), int(w2), 0, int(w4), iodictionary)
        processlist.append(process)
        process = Process(iterador, int(w0), int(w1), int(w2), int(w2), 0, int(w4), iodictionary)
        processlistb.append(process)

        iterador += 1
        
if politica == "PrioNotPreentive":
    run_schedule_nonpreempt()
    run_schedule_preempt()
elif politica == "PrioPreentive":
    run_schedule_preempt()
    run_schedule_nonpreempt()
else:
    print("SCHEDULING INVALIDO")
    sys.exit()

print ("========================COMPARACIONES==============================")
print ("PREEMPTIVE ", "AVG TURNAROUND: ", turnar2, " AVG WAIT TIME: ", waitavg2)
print ("NONPREEMPTIVE ", "AVG TURNAROUND: ", turnar, " AVG WAIT TIME: ", waitavg)
if (turnar2+waitavg2)/2.0 > (turnar + waitavg)/2.0:
    print("NONPREEMPTIVE es mas eficiente")
elif (turnar2+waitavg2)/2.0 < (turnar + waitavg)/2.0:
    print("PREEMPTIVE es mas eficiente")
else:
    print("EMPATE")
