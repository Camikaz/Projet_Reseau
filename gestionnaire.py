import socket
import sys
import pickle
import os

port = int(sys.argv[1])

TAILLE_BLOC=1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(('',port))
s.listen(5)

def connexion_serveur(IP_serveur,port_serveur) :
  print "je me connecte a un serveur sur le port ",port_serveur
  s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s1.connect((IP_serveur ,int(port_serveur)))
  s1.send("fais moi un calcul")
  answer = s1.recv(255)
  print answer
  s.shutdown(1)
  s.close()
  print answer
  

def connexion_client(sockClient) :
  params_bytes = sockClient.recv(TAILLE_BLOC) #Reception in bytes
  params = pickle.loads(params_bytes)  #Transformation in table
  print "recu : ", params
  
  a_min = float(params[0])
  a_max = float(params[1])
  a_pas = float(params[2])
  b_min = float(params[3])
  b_max = float(params[4])
  b_pas = float(params[5])
  
  nb_calculs = int(((a_max-a_min)/float(a_pas))*((b_max-b_min)/float(b_pas)))
  sockClient.send(str(nb_calculs))
  confirmation = bool(sockClient.recv(TAILLE_BLOC))
  print "A-t-on la confirmation du client ? ", confirmation
  if confirmation :
    print "on lance le calcul"
    connexion_serveur("127.0.0.1",port+1)
    connexion_serveur("127.0.0.1",port+2)  
  sockClient.shutdown(1)
  sockClient.close()
  
while True :
  sockClient, addr = s.accept()
  print "Connexion entrante"
  connexion_client(sockClient)
  print "fin de la connexion avec le premier client, on arrete tout"
  s.shutdown(1)
  s.close()


