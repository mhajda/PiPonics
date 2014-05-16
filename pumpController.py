import RPi.GPIO as GPIO ## Import GPIO Library
import time ## Import 'time' library.  Allows us to use 'sleep'
import datetime
import FileLogger

# Start File Logger
global logger
logger = FileLogger.startLogger("/var/www/pumpController.log", 5000, 5)
logger.info("Starting Logger...")

logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + "Script Started" )
time.sleep(1)

GPIO.setmode(GPIO.BCM) ## Use Broadcom pin numbering
gpio_pump=24
gpio_drain=18

GPIO.setwarnings(False)
GPIO.setup(gpio_pump, GPIO.OUT) 
GPIO.output(gpio_pump, True) 
GPIO.setup(gpio_drain, GPIO.OUT) 
GPIO.output(gpio_drain, True) 

script_path = "/home/pi/Aquaponics/PiPonics/"
pump_file = script_path + "pump.txt"
drain_file = script_path + "drain.txt"

with open(pump_file, "r+") as fo:
	fo.seek(0, 0)
	fo.write("0")
fo.closed
	
with open(drain_file, "r+") as fo:
	fo.seek(0, 0)
	fo.write("0")
fo.closed

## Define function named Blink()
def pumpcycle(pump_time,hold_time,drain_time,pause_time,cycle_count):
	if cycle_count == 0:
		cycle_count=999
	
	for i in range(0,cycle_count): ## Run loop numTimes
		## Pump Cycle
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Pump On for " + str(pump_time*60)
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Pump On for " + str(pump_time*60) )
		GPIO.output(gpio_pump, False) ## Turn on pump
		with open(pump_file, "r+") as fo:
			fo.seek(0, 0)
			fo.write("1")
		fo.closed
		
		time.sleep(pump_time*60) ## pump timer
		
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Pump Off "
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Pump Off ")
		GPIO.output(gpio_pump, True) ## Switch off GPIO 
		with open(pump_file, "r+") as fo:
			fo.seek(0, 0)
			fo.write("0")
		fo.closed

		
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Growbed Hold for " + str(hold_time*60)
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Growbed Hold for " + str(hold_time*60))

		time.sleep(hold_time*60) ## Wait

		## Drain Cycle
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Drain On for " + str(drain_time*60)
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Drain On for " + str(drain_time*60))
		GPIO.output(gpio_drain, False) ## Turn on pump
		with open(drain_file, "r+") as fo:
			fo.seek(0, 0)
			fo.write("1")
		fo.closed
		
		time.sleep(drain_time*60) ## pump timer

		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Drain Off " 
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Drain Off " )
		GPIO.output(gpio_drain, True) ## Switch off GPIO
		with open(drain_file, "r+") as fo:
			fo.seek(0, 0)
			fo.write("0")
		fo.closed
		
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Hold for " + str(pause_time*60) 
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Hold for " + str(pause_time*60) )

		time.sleep(pause_time*60) ## Wait

	print "Done" ## When loop is complete, print "Done"
	GPIO.cleanup()

## Prompt user for input
pump_time_input = raw_input("Minutes to run pump: ")
hold_time_input = raw_input("Minutes to hold in grow bed: ")
drain_time_input = raw_input("Minutes to drain: ")
pause_time_input = raw_input("Minutes to wait for next cycle: ")
cycle_count_input = raw_input("How many cycles: ")

pumpcycle(float(pump_time_input),float(hold_time_input), float(drain_time_input),float(pause_time_input),int(cycle_count_input))
