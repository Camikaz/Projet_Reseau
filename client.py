#//////////////////////// Lancement ////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

#Pour lancer en local : python Client.py '127.0.0.1' 7993
#Lancer en deuxieme, apres le gestionnaire.
#Bien mettre un numero de port juste inferieur a celui des processeurs et le
#meme que le gestionnaire


#//////////////////////// Imports //////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
import socket 
import sys
import pickle


#//////////////////////// Programme ////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

#///// IP et port /////
IP_gestionnaire = sys.argv[1] #Entrer '107.0.0.1' PAS PLUTOT 127 ?
port = sys.argv[2] #Entrer 8000

#///// Ouverture de la socket de communication avec le gestionnaire /////
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connect")
s.connect((IP_gestionnaire ,int(port)))


#///// Renseignement des parametres au clavier /////

print '\n////////// GIVE ME YOUR PARAMETERS //////////'

"""
a_min = raw_input('\na_min ? ') #1
a_max = raw_input('a_max ? ')
a_pas = raw_input('pas de a ? ')
b_min = raw_input('b_min ? ')
b_max = raw_input('b_max ? ')
b_pas = raw_input('pas de b ? ')
iterationsServ1_step1 = raw_input('Iter serv1 step 1 ? ') #10
iterationsServ2_step1 = raw_input('Iter serv2 step 1 ? ') #20
iterationsServ1_step2 = raw_input('Iter serv1 step 2 ? ') #30
iterationsServ2_step2 = raw_input('Iter serv2 step 2 ? ') #40
iterationsServ1_step3 = raw_input('Iter serv1 step 3 ? ') #50
iterationsServ2_step3 = raw_input('Iter serv2 step 3 ? ') #60
nombreServeurs = raw_input('Nombre de serveurs a utiliser ?') #2
"""

a_min = 1
a_max = 10
a_pas = 1
b_min = 3
b_max = 100
b_pas = 1
iterationsServ1_step1 = 10
iterationsServ2_step1 = 20
iterationsServ1_step2 = 30
iterationsServ2_step2 = 40
iterationsServ1_step3 = 50
iterationsServ2_step3 = 60
nombreServeurs = 2




#params = [a_min , a_max , a_pas , b_min , b_max , b_pas]
params = [a_min , a_max , a_pas , b_min , b_max , b_pas, iterationsServ1_step1, iterationsServ2_step1, iterationsServ1_step2, iterationsServ2_step2, iterationsServ1_step3, iterationsServ2_step3, nombreServeurs]

#///// Envoie des parametres au gestionnaire /////
#Serialization (transformation in bytes)
params_bytes = pickle.dumps(params) #data loaded
s.send(params_bytes) #send data

#///// Reception du temps estime /////
estimated_time = s.recv(255)


print '\n///////// LANCEMENT DES OPERATIONS /////////'
print "Besoin de faire ", estimated_time, " calculs."
confirmation = raw_input("Lancement des calculs ? Verifiez que vos clients soient prets. (o/n)")
if confirmation == 'o' :
  s.send ("True")
else :
  s.send("False")
  
resultat_bytes=s.recv(1024) #Reception in bytes
resultat = pickle.loads(resultat_bytes)
print "Solution finale : ", resultat

s.close()
