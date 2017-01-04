#//////////////////////// Lancement ////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

#Pour lancer en local : python gestionnaire.py 7993
#Lancer en premier.
#Bien mettre un numero de port juste inferieur a celui des processeurs et le
#meme que le Client


#//////////////////////// Imports //////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
import socket
import sys
import pickle
import os
import threading

from multiprocessing.pool import ThreadPool


#//////////////////////// Programme ////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

port = int(sys.argv[1])

TAILLE_BLOC=1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(('',port))
s.listen(5)

tabThread = []

def thread (tabThread, nombreServeurs, a_min, iterationsServStep):
	loopEnd = True
	result=[]
	while loopEnd:
		
		#Iteration selon le nombre de calculs
		for i in xrange(0, len(iterationsServStep)) :
			
			#///// Envoi des calculs a chaque serveur disponible /////
			print '\n/// Nouveau calcul ///'
			paramsCalcul = [a_min, iterationsServStep[i]]
			paramsCalcul_bytes = pickle.dumps(paramsCalcul) #data loaded
			tabThread[(i+1)%2].send(paramsCalcul_bytes)
			print 'Envoye'
			
			#///// Answer from serveur /////
			answer_bytes = tabThread[(i+1)%2].recv(TAILLE_BLOC)
			answer = pickle.loads(answer_bytes)  #Transformation in table
			print "Le port ", answer[0], " donne le resultat a = ", answer[1], ".\n"
			result.append(answer[1])

 		loopEnd=False 
 		for i in range(nombreServeurs):
			tabThread[i].send("end")
		return result

				

	#return msg



#def connexion_serveur(IP_serveur, port_serveur, paramsCalcul, nombreServeurs, iterationsServStep, a_min) :

def connexion_serveur(IP_serveur, nombreServeurs, iterationsServStep, a_min) :
  
  
	tabSocket = [] #Communication gestionnaire vers serveur
	#tabThread = [] #Communication serveur vers gestionnaire
	
	#///// Creation d'un thread pour chaque serveur /////
	for k in xrange(nombreServeurs) :
		numPort = port+k+1
		
		s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tabSocket.append(s1)
		
		s1.bind((IP_serveur,numPort))
		s1.listen(5)
		s2, addr = s1.accept()
		tabThread.append(s2)
		
		print "Je me connecte a ce serveur sur le port ",numPort, "."
	
	#///// Lancement des calculs par ces threads /////
	pool = ThreadPool(processes=1)
	async_result = pool.apply_async(thread, (tabThread,nombreServeurs,a_min,iterationsServStep))
	#t = threading.Thread(target = thread, args = (tabThread,nombreServeurs,a_min,iterationsServStep,))
	#t.start()
	#stop = True
	#t.join()
	return async_result.get()
		

		
	
	
	
	#///// Envoi d'un nouveau calcul a un serveur inoccupe /////
	#for j in xrange(nombreServeurs+1, len(iterationsServStep)):
	#	tabSocket[i%nombreServeurs]
	#	s1.send(paramsCalcul_bytes) #send data
  
		
		#numServeur = int(i)% nombreServeurs +1
		#print '\n//////// STEP ', int(i+1), ' - SERVEUR ', int(numServeur), ' - PORT ', numPort, '  ///////'
		#print "Le serveur ", numServeur, " recoit les parametres : ", paramsCalcul
		
  
  
  #///// Send parameters to serveur /////
  
  #///// Answer from serveur /////
  #answer_bytes = s1.recv(TAILLE_BLOC)
  #answer = pickle.loads(answer_bytes)  #Transformation in table
  #print "Le port ", answer[0], " donne le resultat a = ", answer[1], ".\n"
  
  #///// Fermeture du socket s1 /////
  #s1.shutdown(1)
  #s1.close()

def connexion_client(sockClient) :
	
	#///// Reception des parametres donnes par le client par clavier /////
  params_bytes = sockClient.recv(TAILLE_BLOC) #Reception in bytes
  params = pickle.loads(params_bytes)  #Transformation in table
  print "Parametres recus : ", params
  
  a_min = float(params[0])
  a_max = float(params[1])
  a_pas = float(params[2])
  b_min = float(params[3])
  b_max = float(params[4])
  b_pas = float(params[5])
  iterationsServ1_step1 = float(params[6]) #Nombre d'iterations de calculs a faire sur le serveur 1 pour le calcul 1, c'est un exemple de traitement
  iterationsServ2_step1 = float(params[7])
  iterationsServ1_step2 = float(params[8])
  iterationsServ2_step2 = float(params[9])
  iterationsServ1_step3 = float(params[10])
  iterationsServ2_step3 = float(params[11])
  nombreServeurs = int(params[12])
  iterationsServStep = [iterationsServ1_step1, iterationsServ2_step1, iterationsServ1_step2, iterationsServ2_step2, iterationsServ1_step3, iterationsServ2_step3]
  
  
  #///// Estimation du nombre de calculs necessaires /////
  nb_calculs = int(((a_max-a_min)/float(a_pas))*((b_max-b_min)/float(b_pas)))
  sockClient.send(str(nb_calculs))
  confirmation = bool(sockClient.recv(TAILLE_BLOC))
  
  
  #///// Repartition des calculs aux clients /////
  print "A-t-on la confirmation du client ? ", confirmation

  if confirmation :
    print "On lance le calcul. Connectez vos clients dans l'ordre croissant des numeros de port."
    #On pourrait ensuite attendre dans le gestionnaire qu'on ait connecte tous
    #les serveurs voulus avec un ok qui termine la tache.
    
    results=connexion_serveur('127.0.0.1', nombreServeurs, iterationsServStep, a_min)
    print(results)
    results_bytes = pickle.dumps(results) #data loaded
    sockClient.send(results_bytes)
    print "Resultats envoyes au client"
    
    
		
		
	
	#///// Fermeture de la socket sockClient /////
  sockClient.shutdown(1)
  sockClient.close()


while True :
  sockClient, addr = s.accept()
  
  print "\n//////// CONNEXION AVEC LE CLIENT ///////\n"
  print "Connexion avec le client etablie."
  connexion_client(sockClient)
  print "Fin de la connexion avec le client et de la procedure."
  break

s.shutdown(1)
s.close()


<<<<<<< HEAD
#192.168.1.12
=======
#192.168.1.12
>>>>>>> origin/master
