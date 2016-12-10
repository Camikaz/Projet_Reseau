#//////////////////////// Lancement ////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

#Pour lancer en local : 
#Serveur 1 : python serveur.py 7994
#Serveur 2 :python serveur.py 7995
#Lancer en dernier.
#Bien mettre des ports juste superieurs a ceux de gestionnaire et Client.

#//////////////////////// Imports //////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
import socket
import sys
import pickle



#//////////////////////// Programme ////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

IP_serveur = sys.argv[1]
port = int(sys.argv[2])
TAILLE_BLOC=1024 

#///// Ouverture de la socket de communication avec le gestionnaire /////
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#s.bind(('',port))
#s.listen(5)
s.connect((IP_serveur,port))


def connexion_gestionnaire(sockGestionnaire) :
	print 'ok'
	#///// Reception des parametres de calculs a effectuer /////
	requete_bytes = sockGestionnaire.recv(TAILLE_BLOC) #Reception in bytes
	#/// ERROR : NE RECOIT PAS LE RECV, ALORS QUE LA CONNEXION EST FAITE ET QUE
	#LE GESTIONNAIRE ARRIVE A ENVOYER DANS LE THREAD ///
	print 'ok'
	
	requete = pickle.loads(requete_bytes)  #Transformation in table
	print "Recu : ",requete
	
	#///// Calcul /////
	a = 1000
	for i in xrange(int(requete[1])) :
		a = int(a - requete[0])
	print "Fin de la tache, a = ",a, "."
	
	#///// Retour de la reponse au gestionnaire /////
	reponse_tab = [port,a]
	reponse_bytes = pickle.dumps(reponse_tab) #data loaded
	sockGestionnaire.send(reponse_bytes) #send data
	print 'Rep envoyee'
	
	#///// Fermeture de la socket /////
	#sockGestionnaire.shutdown(1)
	#sockGestionnaire.close()


while True :
  #sockGestionnaire, addr = s.accept()
  #sockGestionnaire = s
  print "\n////////////// CONNEXION AVEC LE GESTIONNAIRE //////////////"
  print "Connexion avec le gestionnaire etablie."
  #connexion_gestionnaire(sockGestionnaire)
  connexion_gestionnaire(s)
  print "Fin de la connexion avec le gestionnaire.\n"
  s.shutdown(1)
  s.close()
  #sockGestionnaire.shutdown(1)
  #sockGestionnaire.close()
