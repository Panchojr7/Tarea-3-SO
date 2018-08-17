############################
#### Francisco Rousseau ####
######## 201573546-8 #######
############################

import threading
from time import sleep
import time


'''Semaforos by fases'''

## Fase 1 ##    ->    Uso del wc con riesgo de no tener papel higienico
fase1 = threading.Semaphore(1) 
shit = threading.Semaphore(10)
cs = threading.Semaphore(1) #cs = Clean Staff

## Fase 2 ##    ->    Uso del lavamanos
fase2 = threading.Semaphore(1)
wash = threading.Semaphore(5)

## Fase 3 ##   ->     Uso del secador de manos
fase3 = threading.Semaphore(1)
dry = threading.Semaphore(2)


def escribir(id1,id2,ctrl):
	alumnos = open ("clientes.txt", "a")
	personal = open ("personal.txt", "a")
	student = str(id1)
	thing = str(id2)
	if ctrl == 1:
		alumnos.write("> Student N° "+student+" enters the cubicle "+thing+" at "+time.strftime("%H:%M:%S")+"\n")

	elif ctrl == 2:
		alumnos.write("* Student N° "+student+" warns that there is no toilet paper "+thing+" "+time.strftime("%H:%M:%S")+"\n")

	elif ctrl == 3:
		personal.write("* Cleaning staff replenishes toilet paper of Student N° "+student+" "+time.strftime("%H:%M:%S")+"\n")

	elif ctrl == 4:
		alumnos.write("< Student N° "+student+" leaves the cubicle "+thing+" at "+time.strftime("%H:%M:%S")+"\n")

	elif ctrl == 5:
		alumnos.write("|| Student N° "+student+" uses the sink "+thing+" at "+time.strftime("%H:%M:%S")+"\n")

	elif ctrl == 6:
		alumnos.write("|| Student N° "+student+ " stop using the sink "+thing+" at "+time.strftime("%H:%M:%S")+"\n")

	elif ctrl == 7:
		alumnos.write("# Student N° "+student+" uses the hand dryer  "+thing+" at "+time.strftime("%H:%M:%S")+"\n")

	elif ctrl == 8:
		alumnos.write("## Student N° "+student+" stop using the hand dryer "+thing+" at "+time.strftime("%H:%M:%S")+"\n")


'''Variables'''

alum=0 #cantidad de alumnos, max 25
ph=[10,10,10,10,10,10,10,10,10,10]
cubiculos=[0,1,2,3,4,5,6,7,8,9]
lavabos=[0,1,2,3,4] 
secador=[0,1] #Cantidad de secador de manos
n=0 #Controlador de clientes


#######funciones y hebras########

class alumno(threading.Thread):
	def __init__(self, id):
		threading.Thread.__init__(self)
		self.id = id  # Cada self.id corresonde a un alumno

	def run(self):
		global n
		wc(self.id)
		n=n+1

def wc(usuario):
	global lavabos
	global cubiculos
	global ph
	global secador
	global n

	######## Fase 1 ########
	fase1.acquire()
	shit.acquire()
	key = cubiculos[0]
	del cubiculos[0]
	fase1.release()
	escribir(usuario, key, 1)

	if ph[key]== 0:
		escribir(usuario, key, 2)
		cs.acquire()
		sleep(1)
		escribir(usuario,0,3)
		ph[key]=3
		cs.release()
	else:
		ph[key] -=1
	sleep(5)
	cubiculos.append(key)
	shit.release()
	escribir(usuario, key, 4)


	######## Fase 2 ########
	wash.acquire()
	fase2.acquire()
	llave = lavabos[0]
	del lavabos[0]
	fase2.release()
	escribir(usuario, llave, 5)
	sleep(5)
	lavabos.append(llave)
	wash.release()
	escribir(usuario, llave, 6)


	######## Fase 3 ########
	dry.acquire()
	fase3.acquire()
	pos= secador[0]
	del secador[0]
	fase3.release()
	escribir(usuario, pos, 7)
	sleep(2)
	secador.append(pos)
	dry.release()
	escribir(usuario, pos, 8)




###Funcion del thread de la tia del aseo.
def tia():
	global n
	global alum
	students=[]
	while alum >25 or alum==0:
		alum= int(input( "Enter a number of Students: "))

	##### Crear lista de clientes####
	i=0
	while i<alum:
		students.append(alumno(i+1))
		i+=1
	i=0
	##activar las hebras de los alumnos##
	for x in students:
		p=i+1
		alumnos= open ("clientes.txt", "a")
		if x != students[-1]:
			alumnos.write("Student N° "+str(p)+" arrives the bathroom at "+time.strftime("%H:%M:%S")+"\n")
		else:
			alumnos.write("Student N° "+str(p)+" arrives the bathroom at "+time.strftime("%H:%M:%S")+"\n\n")
		alumnos.close()
		x.start()
		i+=1
	while n <alum:
		n
	if n== alum:
		print("-------------------")
		print("si/no")
		respuesta= str(input( "¿llegan mas alumnos? "))
		while  respuesta != "si" and respuesta != "no":
			respuesta= str(input( "¿llegan mas alumnos? "))
		if respuesta== "si":
			n=0
			alum=0
			tia()
		if respuesta=="no":
			print("FIN DEL PROGRAMA")



####################################### Main #######################################
reset = open("personal.txt", "w")
reset.close()
reset= open("clientes.txt", "w")
reset.close()

tia_aseo=threading.Thread(target=tia)
personal = open ("personal.txt","a")
personal.write("Tia del aseo llego a trabajar "+time.strftime("%H:%M:%S")+"\n")
personal.close()
tia_aseo.start()


