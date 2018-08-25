############################
#### Francisco Rousseau ####
######## 201573546-8 #######
############################

from time import sleep
import time
import threading

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

alumnos = open ("clientes.txt", "a")
personal = open ("personal.txt", "a")

def escribir(id1,id2,ctrl):
	global alumnos
	global personal

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

ps = 0 #personas
aeb = 0 #alumnos en el banio


'''Estructuras'''
cubiculos = [0,1,2,3,4,5,6,7,8,9]
ph = [10,10,10,10,10,10,10,10,10,10] #Papel Higienico por cada cubiculo
lavabos = [0,1,2,3,4]
secadores = [0,1] #Cantidad de secadores de manos



''' Thread alumnos que entran al banio '''

class alumno(threading.Thread):
	def __init__(self, id):
		threading.Thread.__init__(self)
		self.id = id 

	def run(self):
		global ps
		wc(self.id)
		ps+=1

''' Funcion de todo lo que acontece en el banio (1313) '''

def wc(usuario):

	'''Variables Globales'''
	global lavabos
	global cubiculos
	global ph
	global secadores

	######## Fase 1 ########
	fase1.acquire()
	shit.acquire()
	articulo = cubiculos[0]
	del cubiculos[0]
	fase1.release()
	escribir(usuario, articulo, 1)

	if ph[articulo] == 0:
		escribir(usuario, articulo, 2)
		cs.acquire()
		sleep(1)
		escribir(usuario,0,3)
		ph[articulo] = 3
		cs.release()
	else:
		ph[articulo] -= 1
	sleep(5)
	cubiculos.append(articulo)
	shit.release()
	escribir(usuario, articulo, 4)


	######## Fase 2 ########
	wash.acquire()
	fase2.acquire()
	articulo = lavabos[0]
	del lavabos[0]
	fase2.release()
	escribir(usuario, articulo, 5)
	sleep(5)
	lavabos.append(articulo)
	wash.release()
	escribir(usuario, articulo, 6)


	######## Fase 3 ########
	dry.acquire()
	fase3.acquire()
	articulo = secadores[0]
	del secadores[0]
	fase3.release()
	escribir(usuario, articulo, 7)
	sleep(5)
	secadores.append(articulo)
	dry.release()
	escribir(usuario, articulo, 8)



''' Funcion correspondiente al personal del aseo'''
''' Usada para llamar a lo anterior '''

def Aseo():

	#Variables Globales#
	global ps
	global aeb

	students=[]
	while aeb >25 or aeb == 0:
		aeb= int(input( "Enter a number of Students: "))

	'''Lista de estudiantes '''
	s=0
	while s < aeb:
		students.append(alumno(s+1))
		s+=1
	


	''' Llegada al banio e inicio del thread '''
	c=0
	for persona in students:
		pers=c+1

		if persona != students[-1]:
			alumnos= open ("clientes.txt", "a")
			alumnos.write("Student N° "+str(pers)+" arrives the bathroom at "+time.strftime("%H:%M:%S")+"\n")
		else:
			alumnos= open ("clientes.txt", "a")
			alumnos.write("Student N° "+str(pers)+" arrives the bathroom at "+time.strftime("%H:%M:%S")+"\n\n")

		alumnos.close()
		persona.start()
		c+=1

	while ps <aeb:
		ps

	if ps == aeb:

		flag= True

		while flag:
			print("\n0.- Yes\n1.- No")
			asw= str(input( "More Students use the bathroom?\n"))
			if asw == '0' or asw=='1':
				flag = False


		if asw == '0':
			aeb = 0
			ps = 0
			Aseo()

		else:
			print("Goodbye good man, have a nice day!")
			sleep(1)



####################################### Main #######################################

''' Limpieza de archivos '''
reset = open("personal.txt", "w")
reset.close()
reset= open("clientes.txt", "w")
reset.close()

''' Sra Juanita reportandose al llamado del deber '''
personal = open ("personal.txt","a")
personal.write("Cleaning Staff starts to work"+time.strftime("%H:%M:%S")+"\n")
personal.close()

''' This part of my life, this little part... is called happiness '''
aseo=threading.Thread(target=Aseo)
aseo.start()


