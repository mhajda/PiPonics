import logging
import logging.handlers
import time

#import ntplib
#import os

def startLogger(filename, maxBytes, backupCount):

	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)

	# create a file handler
	#handler = logging.FileHandler(filename)
	handler = logging.handlers.RotatingFileHandler(filename, 'a', maxBytes, backupCount)
	handler.setLevel(logging.INFO)

	# create a logging format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	# add the handlers to the logger
	logger.addHandler(handler)
	
	return logger

def main():

	global logger

	logger = startLogger('hello.log', 100000, 5)

	#logger.info("date")
	#logger.info(os.popen("date").read())
	
	#logger.info("export")
	#logger.info(os.popen("export").read())

	#logger.info("cat .profile")
	#logger.info(os.popen("cat .profile").read())

	for i in range(60):
		#c = ntplib.NTPClient()
		#response = c.request('europe.pool.ntp.org', version=3)
		#print(time.ctime(response.tx_time))
		#logger.info(time.ctime(response.tx_time))
				
		print('Hello ' + str(i))
		logger.info('Hello ' + str(i))
		time.sleep(1)

	try:
		print x

	except Exception, e:
		logger.error('Failed to open file', exc_info=True)

	test()

def test():
	global logger

	try:
		print y
	except Exception, e:
		logger.error('Failed to open file', exc_info=True)
		
    
if __name__ == '__main__':
	main()