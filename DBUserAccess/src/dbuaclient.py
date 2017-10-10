"""
Implements dbua program's main logic 
"""


import strs
from logs import Log
from helpers import Helpers

from configuration import ConfigReader
from databases import *
from query import *
from dumpers import DumpResult
from dbua import Dbua
from providers  import DatabaseProvider



class DbuaClient(object):
	"""
	Implements DBUA client logics
	"""

	# global variables
	log_level = 0 

	def __init__(self):
		"""
		All initialization for the client program is done here
		"""
		self.log_level = ConfigReader.getLogLevel()

		#debug-mode
		Helpers.displayText('Log level : ' + self.log_level)
		Log.writeLog('Log level : ' + str(self.log_level), strs.INFO)
		#debug-mode


		# get meta server connection
		meta_svr_con_para_dict =  ConfigReader.getMetaSvrAccessPara()
		database_provider = DatabaseProvider()
		metaserver_db_obj = database_provider.getDatabase(strs.metaserver_db_type)
		if not metaserver_db_obj :
			Log.writeLog('meta server object creation failed', strs.ERRO)
			raise SystemExit('meta server object creation failed')

		# decrypt password
		meta_svr_con_para_dict['password'] = Helpers.scramblePwd(strs.decrypt, '', meta_svr_con_para_dict['password'])

		meta_svr_con = metaserver_db_obj.getDbConnection(meta_svr_con_para_dict)		

		if not meta_svr_con : 
			Log.writeLog('meta server database connection failed', strs.ERRO)			
			raise SystemExit('meta server database connection failed. ')
		Log.writeLog('connected to metaserver', strs.INFO)			



		#
		# get gloabl-list for query run: global_task_list
		#
		global_task_list = []
		query = Query()
		global_task_list_resultset = query.executeQuery(strs.global_query, meta_svr_con)

		if global_task_list_resultset == 0:
			# if there exception on query execution
			# we comapre it with zero (0) value of the resultset.
			raise SystemExit('global query execution failed. \n Quey : ' + strs.global_query)

		
		# exit if the query result set is empty
		# we compare using python not operator to verigy the empty resultset				
		if not global_task_list_resultset :
			Log.writeLog('global_query returned empty result.', strs.INFO)
			raise SystemExit('global_query returned empty result.  \n Quey : ' + strs.global_query)


		global_task_list_resultset_cols = query.getColumnsList(global_task_list_resultset)

		# debug-code		
		if self.log_level == strs.log_level_high :			
			Log.writeLog(global_task_list_resultset_cols, strs.INFO) 
		# debug-code
		
		# convert result set to list of dictionaries
		resultset_dict_list = self.resultsetToDictList(global_task_list_resultset, global_task_list_resultset_cols)
	
		if self.log_level == strs.log_level_high :			
			Helpers.printList(resultset_dict_list)
			Log.writeLog(resultset_dict_list, strs.INFO)


		#------------------------------------------------------------
		# 		FETCHING TASK IS SUCCESSFUL
		#------------------------------------------------------------

		#
		# run dbua operation
		# 

		dbua = Dbua(resultset_dict_list)
		dbua.rundbuaOps()

		Helpers.displayText('Script completed!')
		Log.writeLog('Script completed!', strs.INFO)
		# close connection
		meta_svr_con.close()		


	def resultsetToDictList(self, input_resultset, global_task_list_resultset_cols):
		"""
		Helper module to convert resultset to rows of python dictionary
		"""
		resultset_dict_list = []

		try:
			for row in input_resultset.fetchall():
				resultset_dict_list.append(dict(zip(global_task_list_resultset_cols, row)))
		except Exception, e:
			Log.writeLog('Exception on DbuaClient.resultsetToDictList module. Msg : ' + str(e), strs.ERRO)
			raise SystemExit('Exception on DbuaClient.resultsetToDictList module. Msg : ' + str(e))
		
		return resultset_dict_list




















		



