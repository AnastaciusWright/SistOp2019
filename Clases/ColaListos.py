from Clases.Procesos import *
#from Clases.Procesador import *

class ColaListos:
    def __init__(self):
        self.cola_listos=[]

    # Setters

    # Getters
    def get_cola_listos(self):
        return self.cola_listos

    # Funciones
    def anade_proceso(self, proc):
        self.cola_listos.append(proc)

    def fcfs(self,procesador):
        #self.cola_listos
       
        #None es el quatum, en este caso no nos interesa
        procesador.listos_ejecucion(None)
        procesador.bloqueados_listos()
        procesador.imprime_cola_listos()
        procesador.imprime_cola_bloqueados()

        

    def prioridades(self, procesador):
        self.cola_listos.sort(key=lambda x: x.get_prioridad(), reverse=True)
        procesador.bloqueados_listos()
        procesador.listos_ejecucion(None)
        procesador.imprime_cola_bloqueados()
        procesador.imprime_cola_listos()

    def imprimir_consola(self):
        for x in self.cola_listos:
            x.print_proceso_fake()

    def multinivel(self, CL1, CL2, CL3, procesador):
        for proc in self.get_cola_listos():
            tiempo_uso_cpu = 0
            for rafaga in (proc.get_rafaga_tot()):
                if rafaga[0] == "C":
                    tiempo_uso_cpu = tiempo_uso_cpu + int(rafaga[1])
            if tiempo_uso_cpu < 10:
                CL1.anade_proceso(proc)
            elif tiempo_uso_cpu < 20:
                CL2.anade_proceso(proc)
            else:
                CL3.anade_proceso(proc)

        # de esta forma, se ejecuta primero todo lo de la cola 1, despues todo lo de la cola 2,etc
        if CL1 != []:
            CL1.round_robin(5, procesador)
        elif CL2 != []:
            CL2.round_robin(3, procesador)
        else:
            CL3.fcfs(procesador)

    def elimina_elemento(self, num):
        self.cola_listos.pop(num)

    def round_robin(self, quantum, procesador):

        # self.quantum = quantum
        aux = procesador.get_proceso_actual()
        if aux != None:
            tiempo_r = aux.get_tiempo_restante()
            q = procesador.get_proceso_actual().get_quantum()
            print("q1"+str(q))
            if tiempo_r > 0 and q > 0: #No termino ni el quantum ni el tiempo restante
                print(">>>> aux != None and tiempo_r > 0 and q >0  <<<<")
                # tiempo_r -=1
                q -= 1
                # aux.set_tiempo_restante(tiempo_r)
                aux.set_quantum(q)

                print("quantum1 actual : "+str(aux.get_quantum()))
                print(procesador.get_proceso_actual().get_quantum())
                print("Tiempo restante del proceso actual : " +str(aux.get_tiempo_restante()))
                procesador.bloqueados_listos()
                procesador.set_proceso_actual(aux)
                procesador.imprime_cola_bloqueados()
                procesador.imprime_cola_listos()
            elif tiempo_r > 0 and q == 0: # se acabo el quantum
                print(">>>> aux != None and tiempo_r > 0 and q == 0 <<<<")
                # tiempo_r -= 1
                # aux.set_tiempo_restante(tiempo_r)
                print("quantum actual : "+str(aux.get_quantum()))
                print("Tiempo restante del proceso actual : " +str(aux.get_tiempo_restante()))
                # se añade el proceso a la cola de listos
                self.modificar_rafaga_total(aux,tiempo_r)
                aux.set_estado(2) #LISTO
                self.anade_proceso(aux)
                self.imprime_cola_listos()
                # Le aplicamos un expropiese venezolano
                procesador.set_proceso_actual(None)
                procesador.listos_ejecucion(quantum)
                procesador.bloqueados_listos()
                procesador.imprime_cola_bloqueados()
                procesador.imprime_cola_listos()
            else:
                if tiempo_r == 0:
                    print("pasa a bloqueado o terminado")
                    procesador.listos_ejecucion(quantum)
                    procesador.bloqueados_listos()
                    procesador.imprime_cola_bloqueados()
                    procesador.imprime_cola_listos()
        else:
            print("################## procesador vacio ###################")
            print(" ")
            procesador.listos_ejecucion(quantum)
            procesador.bloqueados_listos()
            procesador.imprime_cola_bloqueados()
            procesador.imprime_cola_listos()
        return self.cola_listos

    #si band == True, significa que esta en SRTF, si band == False, significa que solo es SJF
    def sjf(self,procesador,band):
        primer_elemento = True
        pos_elem_menor = None
        pos = 0
        for i in self.cola_listos: #avanzamos toda la cola de listos
            rafaga = i.get_rafaga_tot()
            elem_rafaga = rafaga[0]
            if elem_rafaga[0] == "C" and primer_elemento: #solamente el primer elemento
                proceso_menor = i
                pos_elem_menor = pos
                tiempo_menor = int(elem_rafaga[1])
                primer_elemento = False
            elif elem_rafaga[0] == "C" and not(primer_elemento): #el resto de los elementos
                if tiempo_menor >= int(elem_rafaga[1]): #comparamos si tenemos el menor tiempo
                    proceso_menor = i
                    pos_elem_menor = pos
                    tiempo_menor = int(elem_rafaga[1])
            pos +=1

        #agregamos al principio de la cola de listos a nuestro proceso cuya rafaga de ejecucion sea la menor
        #Seria None si no hay procesos cuya rafaga a ejecutarse sea "CPU" o que no haya elementos en Cola de listos
        if pos_elem_menor != None: 
            self.cola_listos.pop(pos_elem_menor)
            self.cola_listos.insert(0,i)

        #luego procedemos a llamar a las funciones de intercambio de colas
        if band == False:
            procesador.listos_ejecucion(None)
            procesador.bloqueados_listos()


    #basicamente lo mismo que el SJF pero con expropiacion
    #si band == True, significa que esta en SRTF, si band == False, significa que solo es SJF
    def srtf(self,procesador,band):
        self.sjf(procesador,band)
        # 1ro verificar si el tiempo de ejecicion restante del proceso que esta en el procesador 
        #es menor al tiempo de ejecucion del proceso que esta en cola de listos (en la 1ra pos)
        cola_listos = self.get_cola_listos()
        proceso_actual = procesador.get_proceso_actual()
        if len(cola_listos) > 0 and proceso_actual != None:
            rafaga_tot = cola_listos[0].get_rafaga_tot()
            num_rafaga = cola_listos[0].get_num_rafaga_actual()
            tiempo_ejecucion = int(rafaga_tot[num_rafaga][1])
            tiempo_restante = proceso_actual.get_tiempo_restante()
            if  tiempo_restante > tiempo_ejecucion:
                #sacamos el proceso del procesador
                self.modificar_rafaga_total(proceso_actual,tiempo_restante)
                self.anade_proceso(proceso_actual)
                procesador.set_proceso_actual(None) 

        #insertamos el proximo proceso en el procesador
        procesador.listos_ejecucion(None)
        procesador.bloqueados_listos()

    def ordenar(self, algoritmo, quantum, CL1, CL2, CL3, procesador):
        if algoritmo == 0:
            self.fcfs(procesador)  
        if algoritmo == 1:
            self.round_robin(quantum, procesador)
        if algoritmo == 2:
            self.prioridades(procesador) 
        if algoritmo == 3:
            self.multinivel(CL1, CL2, CL3, procesador)
        if algoritmo == 4:
            self.sjf(procesador,False)
        if algoritmo == 5:
            self.srtf(procesador,True)

    def isvacio(self):
        return self.cola_listos == []

    def imprime_cola_listos(self):
        print("Procesos listos")
        for x in self.get_cola_listos():
            print("ID: "+str(x.get_id())+" Tiempo Restante " +
                  str(x.get_tiempo_restante()))
        print("----------------")

#solucion momentanea(o permanente je), se modifica la rafaga total cuando q=0
    def modificar_rafaga_total(self,proceso,tiempo_restante):
        num_rafaga = proceso.get_num_rafaga_actual()
        rafaga_total = proceso.get_rafaga_tot()
        rafaga_total[num_rafaga] = "C"+str(tiempo_restante+1)
        proceso.set_rafaga_total(rafaga_total)