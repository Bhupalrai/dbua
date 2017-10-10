
import strs
from logs import Log
from helpers import Helpers


class DBUserAccessMain(object):

	@classmethod
	def startScript(cls,):
		"""
		Start logics from here
		"""
		from configuration import VerifyConfiguration
		from dbuaclient import DbuaClient

		Helpers.displayText('script started')
		Log.writeLog('script started', strs.INFO)
		
		# verify config
		VerifyConfiguration()
		Helpers.displayText('configuration verified')
		Log.writeLog('configuration verified',strs.INFO)

		# start client program
		DbuaClient()

		







		