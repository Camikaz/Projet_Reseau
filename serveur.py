import socket
import sys

port = int(sys.argv[1])
TAILLE_BLOC=1024 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(('',port))
s.listen(5)



def connexion_gestionnaire(sockGestionnaire) :
  requete = sockGestionnaire.recv(TAILLE_BLOC)
  print "recu : ",requete
  sockGestionnaire.send("j'ai realise le calcul souhaite, voici le resultat")
  sockGestionnaire.shutdown(1)
  sockGestionnaire.close()


while True :
  sockGestionnaire, addr = s.accept()
  print "connection entrante"
  connexion_gestionnaire(sockGestionnaire)
  print "fin de la connexion avec le gestionnaire, on arrete tout"
  s.shutdown(1)
  s.close()
