"""
Contains Logging modules
"""

import time
import io
import ConfigParser


class Log(object):

	
	@classmethod
	def writeLog(cls, input_text, msg_category):
		"""
		Write to the log file
		@/var/log/dbuseraccess/dbuseraccess.log file for logging
		"""
		try:
			file = open('/var/log/dbuseraccess/dbuseraccess.log', 'a')
			file.write(str(time.strftime("%Y-%m-%d %H:%M:%S ")) + str(msg_category)+ ' ' +str(input_text)+ '\n')
			file.close()
		except Exception, e:
			print('Exception in Helpers.displayText module. Msg: \n'+str(e))
			


