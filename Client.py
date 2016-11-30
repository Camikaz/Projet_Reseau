import socket 
import sys
import pickle


IP_gestionnaire = sys.argv[1] #Entrer '107.0.0.1'
port = sys.argv[2] #Entrer 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_gestionnaire ,int(port)))
a_min = raw_input('a_min ? ')
a_max = raw_input('a_min ? ')
a_pas = raw_input('pas de a ? ')
b_min = raw_input('b_min ? ')
b_max = raw_input('b_min ? ')
b_pas = raw_input('pas de b ? ')

params = [a_min , a_max , a_pas , b_min , b_max , b_pas]

#Serialization (transformation in bytes)
params_bytes = pickle.dumps(params) #data loaded
s.send(params_bytes) #send data


estimated_time = s.recv(255)

print "on va faire environ  ", estimated_time, " calculs"
confirmation = raw_input("on lance le calcul ? (o/n)")
if confirmation == 'o' :
  s.send ("True")
else :
  s.send("False")

s.close()

