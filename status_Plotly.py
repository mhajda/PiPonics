import os
import glob
import time
import datetime

import plotly # plotly library
import json # used to parse config.json
import time # timer functions

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_file_list = [glob.glob(base_dir + '28*')[0] + '/w1_slave',glob.glob(base_dir + '28*')[1] + '/w1_slave']

script_path = "/home/pi/Aquaponics/prod/"
pump_file = script_path + "pump.txt"
drain_file = script_path + "drain.txt"

username = 'Plot.ly Username'
api_key = 'API_KEY'
stream_token = ['#######','######','######','######']

def initPlotly():
	p = plotly.plotly(username, api_key)

	trace_1 = {'x': [], 'y': [], 'stream': {'token': stream_token[0], 'maxpoints': 5000}}
	trace_2 = {'x': [], 'y': [], 'stream': {'token': stream_token[1], 'maxpoints': 5000}}
	trace_3 = {'x': [], 'y': [], 'stream': {'token': stream_token[2], 'maxpoints': 5000}}
	trace_4 = {'x': [], 'y': [], 'stream': {'token': stream_token[3], 'maxpoints': 5000}}

	print p.plot([trace_1, trace_2, trace_3, trace_4],
		filename='Aquaponics May 15',fileopt='extend')

def read_temp_raw(device_file_no):
	device_file_current=device_file_list[device_file_no]
	f = open(device_file_current, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp(device_file_no):
    lines = read_temp_raw(device_file_no)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file_no)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return round(temp_f,0)

initPlotly()		

stream_1 = plotly.stream(stream_token[0])
stream_2 = plotly.stream(stream_token[1])
stream_3 = plotly.stream(stream_token[2])
stream_4 = plotly.stream(stream_token[3])

while True:
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	pump_status=0
	drain_status=0
	
	with open(pump_file, "r") as fo:
				fo.seek(0, 0)
				pump_status = fo.read(1)
	fo.closed
	
	with open(drain_file, "r") as fo:
				fo.seek(0, 0)
				drain_status = fo.read(1)
	fo.closed
	
	print "checking temp and posting"
	print timestamp + 'Temp 1:' + str(read_temp(0)) + ' Temp 2:' + str(read_temp(1)) + ' Pump:' + str(pump_status) + ' Drain:' + str(drain_status)

	try:
		stream_1.write({'x': timestamp, 'y': read_temp(0)})
		stream_2.write({'x': timestamp, 'y': read_temp(1)})
		stream_3.write({'x': timestamp, 'y': pump_status})
		stream_4.write({'x': timestamp, 'y': drain_status})
		
	except Exception, e:
		print 'Error writing to plot.ly' + str(e)
		initPlotly()

	print 'Sleeping'
	time.sleep(55)
