import os

import glob
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
import RPi.GPIO as GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
arquivo = open('novo-arquivo.txt', 'w')
buzzer= 16 
GPIO.setup(buzzer,GPIO.OUT)
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
min_temp = None	
temp_anterior = None
temp_atual =  [36,99]
while True:
	
        temp_atual = read_temp()
        if temp_atual[0] > 20:
	    #GPIO.output(buzzer,GPIO.HIGH)
	    print("Beep")
#        if temp_atual[0] < temp_anterior:
#            arquivo.write(temp_atual[0])
        
	print(temp_atual)	
	temp_anterior = temp_atual
        time.sleep(1)
	GPIO.output(buzzer,GPIO.LOW)
arquivo.close()
