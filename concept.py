import RPi.GPIO as GPIO
from time import sleep
import smtplib
 
sent_from = #'email@address.here'
to = #'email address or phone here'

subject = 'Raspberry SMTP'
txtoff = 'All sprinklers are OFF.'
txtallon = 'All sprinklers are ON.'
txtquadrant1 = 'Only Quadrant 1 sprinklers are currently ON'
txtquadrant2 = 'Only Quadrant 2 sprinklers are currently ON'
txtquadrant3 = 'Only Quadrant 3 sprinklers are currently ON'
 
 
txtserver = smtplib.SMTP('smtp.gmail.com', 587)
txtserver.ehlo()
txtserver.starttls()
txtserver.login(#'email account', 'password')


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT) #Green
GPIO.setup(23, GPIO.OUT) #Yellow
GPIO.setup(18, GPIO.OUT) #Red
GPIO.setup(17, GPIO.OUT) #Blue
GPIO.setup(12, GPIO.IN) #Button

GPIO.output(17, 0)
GPIO.output(16, 0)
GPIO.output(23, 0)
GPIO.output(18, 0)
press = 0;
count = 0;
prev = 0;
print"press", press
print "START PROGRAM"
try:
	while True: #Carry on until CTRL+C pressed
		button = GPIO.input(12)
		
		if (button == 1) and (button != prev):
				prev = 1
				count = 1
				press += 1
				print"press", press
				sleep(0.25)

		elif (button == 0) and (button != prev):
			prev = 0
			sleep(0.25)
			

		elif (button == 0) and (button == prev):
			
			if (count == 1):
				if (press == 5):
					press = 0
				if( press == 0):
					print"press", press
					GPIO.output(17, 0)
					GPIO.output(16, 0)
					GPIO.output(23, 0)
					GPIO.output(18, 0)
					txtserver.sendmail(sent_from, to, txtoff)
				
				if (press == 1): 
					print"press", press
					GPIO.output(17, 1)
					GPIO.output(16, 1)
					GPIO.output(23, 1)
					GPIO.output(18, 1)
					txtserver.sendmail(sent_from, to, txtallon)
					
				if (press == 2):
					print"press", press
					GPIO.output(17, 1)
					GPIO.output(16, 0)
					GPIO.output(23, 0)
					GPIO.output(18, 1)
					txtserver.sendmail(sent_from, to, txtquadrant1)
					
				if (press == 3):
					print"press", press
					GPIO.output(17, 1)
					GPIO.output(16, 0)
					GPIO.output(23, 1)
					GPIO.output(18, 0)
					txtserver.sendmail(sent_from, to, txtquadrant2)

				if (press == 4):
					print"press", press
					GPIO.output(17, 1)
					GPIO.output(16, 1)
					GPIO.output(23, 0)
					GPIO.output(18, 0)
					txtserver.sendmail(sent_from, to, txtquadrant3)					

				count = 0
				prev = 0
			
finally:
	txtserver.close()
	print"TEXT SERVER CLOSED"
	GPIO.cleanup()
	print "ALL POWERED DOWN"
