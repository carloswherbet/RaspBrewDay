from flask import Flask, render_template
import os
import math
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
import RPi.GPIO as GPIO

app = Flask(__name__)

@app.route('/')

def index():
 #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'panela-html.svg')GPIO.setwarnings(False)


 return render_template("index.html",
  user_image =  os.path.join('static', 'panela-html.svg'), 
  temp_1 = getSensorTemp()
  )
 #return 'Hello world'
def getSensorTemp():
  GPIO.setmode(GPIO.BCM)
  base_dir = '/sys/bus/w1/devices/'
  device_folder = glob.glob(base_dir + '28*')[0]
  device_file = device_folder + '/w1_slave'
  
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
          return round(temp_c,2), temp_f
  return read_temp()
if __name__ == '__main__':

 app.run(debug=True, host='0.0.0.0')
