#!/usr/bin/env python
# Trouve sur domotique-info.fr
import time
import serial
import MySQLdb
import subprocess
from time import sleep
import datetime

paramMysql = {
    'host'   : 'localhost',
    'user'   : 'domotique',
    'passwd' : '*********',
    'db'     : 'domotique'
}

#=========================================================================
# Fonction Tableau/Dictionnaire
#=========================================================================
def checksum (etiquette, valeur):
                sum = 32
                for c in etiquette: sum = sum + ord(c)
                for c in valeur:        sum = sum + ord(c)
                sum = (sum & 63) + 32
                return chr(sum)

#=========================================================================
# Fonction LireTeleinfo
#=========================================================================
def LireTeleinfo ():
		trameOk = False;
		essaiLecture = 10;
		while not trameOk:
			essaiLecture -= 1 
                	# Attendre fin puis le debut du message
			while ser.read(1) != chr(3): pass
                	while ser.read(1) != chr(2): pass

                	message = ""
                	fin = False
                
                	while not fin:
                        	char = ser.read(1)
                        	if char != chr(3):
                                	message = message + char
                        	else:
                                	fin = True
                	
			#print message, "\n --------------"	
			trames = [
                        	trame.split(" ")
                        	for trame in message.strip("\r\n\x03").split("\r\n")
                        	]

			# Check Trame
			trameOk = True           
			for trame in trames:
				if (len(trame) != 3):
					trameOk = False
					print "Err LEN : ", trame
				else:
					sum = checksum(trame[0],trame[1])
					if  (sum != trame[2]):
						trameOk = False
						print "Err SUM : ", trame, " SUM: ", sum, " != ", trame[2]	

			# 10 essai seulelement, sinon on renvoi une erreure
			if essaiLecture < 1:
				print "ERREURLECTURE : 1"
				trameOk = True	
 	
		#print "NBESSAILECT : ", (10 - essaiLecture)
                tramesValides = dict([
                        [trame[0],trame[1]]
                        for trame in trames
                        if (len(trame) == 3) and (checksum(trame[0],trame[1]) == trame[2])
                        ])
                        
                return tramesValides

#=========================================================================
# Connexion au port
#=========================================================================
ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate=1200,
	parity=serial.PARITY_EVEN,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.SEVENBITS )
#=========================================================================
# Definition variables de trame et chargement d'une valeur initiale
#=========================================================================
vIINST = 0 
vMOTDETAT = 0
vOPTARIF = 0
vISOUSC = 0
vADCO = 0
vHCHC = 0
vHCHP = 0
vPAPP = 0
vIMAX = 0
vHHPHC = 0
vBASE = 0
vBBRHCJB = 0
vBBRHPJB = 0
vBBRHCJW = 0
vBBRHPJW = 0
vBBRHCJR = 0
vBBRHPJR = 0
vPEJP = 0
vPTEC = 0
vADPS = 0
#=========================================================================
# Traitement Premiere voie RPIDOM
#=========================================================================
ser.flushInput()
tramesOk = LireTeleinfo()
trouve = False
for etiquette in tramesOk:
    	if etiquette == 'IINST':
        	print etiquette , ":", tramesOk[etiquette]
        	vIINST = tramesOk[etiquette]
	if etiquette ==  'MOTDETAT':
    		print etiquette , ":", tramesOk[etiquette]
    		vMOTDETAT = tramesOk[etiquette]
	if etiquette ==  'OPTARIF':
        	print etiquette , ":", tramesOk[etiquette]
       		vOPTARIF = tramesOk[etiquette]
	if etiquette ==  'ISOUSC':
        	print etiquette , ":", tramesOk[etiquette]
        	vISOUSC = tramesOk[etiquette]
	if etiquette ==  'ADCO':
        	print etiquette , ":", tramesOk[etiquette]
        	vADCO = tramesOk[etiquette]
	if etiquette ==  'HCHC':
    		print etiquette , ":", tramesOk[etiquette]
    		vHCHC = tramesOk[etiquette]
	if etiquette ==  'HCHP':
        	print etiquette , ":", tramesOk[etiquette]
        	vHCHP = tramesOk[etiquette]
	if etiquette ==  'PAPP':
        	print etiquette , ":", tramesOk[etiquette]
        	vPAPP = tramesOk[etiquette]
	if etiquette ==  'IMAX':
        	print etiquette , ":", tramesOk[etiquette]
       	 	vIMAX = tramesOk[etiquette]
	if etiquette ==  'HHPHC':
        	print etiquette , ":", tramesOk[etiquette]
        	vHHPHC = tramesOk[etiquette]
	if etiquette ==  'BASE':
    		print etiquette , ":", tramesOk[etiquette]
    		vBASE = tramesOk[etiquette]
	if etiquette ==  'BBR HC JB':
        	print etiquette , ":", tramesOk[etiquette]
        	vBBRHCJB = tramesOk[etiquette]
	if etiquette ==  'BBR HP JB':
        	print etiquette , ":", tramesOk[etiquette]
        	vBBRHPJB = tramesOk[etiquette]		
	if etiquette ==  'BBR HC JW':
        	print etiquette , ":", tramesOk[etiquette]
        	vBBRHCJW = tramesOk[etiquette]
	if etiquette ==  'BBR HP JW':
        	print etiquette , ":", tramesOk[etiquette]
        	vBBRHPJW = tramesOk[etiquette]
    	if etiquette ==  'BBR HC JR':
    		print etiquette , ":", tramesOk[etiquette]
    		vBBRHCJR = tramesOk[etiquette]
    	if etiquette ==  'BBR HP JR':
        	print etiquette , ":", tramesOk[etiquette]
        	vBBRHPJR = tramesOk[etiquette]
	if etiquette ==  'PEJP':
        	print etiquette , ":", tramesOk[etiquette]
        	vPEJP = tramesOk[etiquette]
	if etiquette ==  'PTEC':
        	print etiquette , ":", tramesOk[etiquette]
        	vPTEC = tramesOk[etiquette]
	if etiquette ==  'ADPS':
	       	print etiquette , ":", tramesOk[etiquette]
	       	vADPS = tramesOk[etiquette]    
#=========================================================================
# Definition des des variables temporelles
#=========================================================================
vHEURE = datetime.datetime.now().strftime('%H:%M')
vDATE = datetime.datetime.today().strftime('%Y-%m-%d')

db = MySQLdb.connect(**paramMysql)
cursor = db.cursor()
cursor.execute("""INSERT INTO conso_teleinfo(DATE, HEURE, IINST, MOTDETAT, OPTARIF, ISOUSC, ADCO, HCHC, HCHP, PAPP, IMAX, HHPHC, BASE, BBRHCJB, BBRHPJB, BBRHCJW, BBRHPJW, BBRHCJR, BBRHPJR, PEJP, PTEC, ADPS)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" ,(vDATE, vHEURE, vIINST, vMOTDETAT, vOPTARIF, vISOUSC, vADCO, vHCHC, vHCHP, vPAPP, vIMAX, vHHPHC, vBASE, vBBRHCJB, vBBRHPJB, vBBRHCJW, vBBRHPJW, vBBRHCJR, vBBRHPJR, vPEJP, vPTEC,vADPS))
# Envoyer dans la base de donnees
db.commit()
db.rollback()
db.close()
#=========================================================================	
ser.close()
