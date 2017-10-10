"""
Fire query to remote server and return the final result
"""

import strs
from logs import Log

from providers import DatabaseProvider
from configuration import ConfigReader
from query import *
from uploaders import Upload
from helpers import Helpers
from databases import OracleDatabase

class Dbua(object):

	global_task_list = []
	global_ouput_list = []

	def __init__(self, global_task_list):
		self.global_task_list = global_task_list

	
	def map_task(self, task):
		"""
		Mapping module to match the dictionary key provided from the databse with 
		the application configuration key names representing the same key. Eg. database_name with DATABASE, 
		uid with username etc.

		rtype: dictionary
		""" 

		try:
			task['server_name'] = task.pop('SERVER')
			task['database_name'] = task.pop('DATABASE_NAME')
			task['user_name'] = task.pop('USERID')
			task['password'] = task.pop('PWD')
			task['sid'] = task.pop('SID')
			task['port'] = task.pop('PORT')
		except Exception, e:
			"""
			Raise system exit when mapping error. Run again after fixing the mapping error
			"""

			Log.writeLog('Exception in Dbua.map_task module. Msg : ' + str(e), strs.ERRO)
			Helpers.displayText('Exception in Dbua.map_task module. Msg : ' + str(e))
			# raise SystemExit('Exception in Dbua.map_task module. Msg : ' + str(e))
			return 0
		return task



	def generateReport(self, input_resultset):
		Log.writeLog('generating report', strs.INFO)
		upload = Upload()
		error_count = upload.uploadOutput(None, input_resultset, None)
		
		if error_count > 0 :
			Helpers.displayText('=========================== ERRORS ========================')
			Helpers.displayText('            Total Error entry while uploading to table : '+ \
				str(error_count) +'   ')
			Helpers.displayText('=========================== ERRORS ========================')
			Helpers.displayText('check log for more details and output/ for invlid entries')		

			return error_count
		else:
			return strs.success	



	def rundbuaOps(self):
		"""
		Core task of Duba module is implemented here.
		retype: list. Report of the result if it fails to upload to database table.
		"""	
		columns = []

		for task in self.global_task_list :
			# 1. get proper db object
			# 2. get connection to the server
			# 3. run query 
			# 4. convert to list, the resultset
			# 5. appent it to the gloabl ouput list
			# 6. return the final list
			
			# get database object
			provider = DatabaseProvider()
			db_object = provider.getDatabase(task['DATABASE_TYPE'])
			# check the object
			if not db_object :
				""" module not available """
				Log.writeLog('module not available for : ' + str(task['DATABASE_TYPE']), strs.ERRO)
				# continue to next task
				continue

			# map database task to application task.
			# Is required to match the  column names
			task = self.map_task(task)
			if not task :
				# if mapping fails
				continue

			# debug-code
			Helpers.displayText('fetching report from : ' + task['database_name'] + '@' + task['server_name'])
			Log.writeLog('fetching report from : ' + task['database_name'] + '@' + task['server_name'], strs.INFO)			
			# debug-code

			# decrypt password
			task['password'] = Helpers.scramblePwd(strs.decrypt, '', task['password'])
			
			db_con = db_object.getDbConnection(task)
			if not db_con :
				""" if connnection fails, continue to next iteration """
				continue

			#
			# run query 
			#
			if task['DATABASE_TYPE'] == strs.db_type_mssql : # mssql specific class, 
				query = MssqlQuery()
			else:
				query = Query()

			resultset = query.executeQuery(task['QUERY'], db_con)
			if not resultset :
				""" if error occurs on executing query , continue to next iteration """
				db_con.close()
				continue

			# compare the query columns, reject if doesnot matches
			if not columns :
				columns = Helpers.getColumnList(resultset)

			
			#debug-code
			#may throw exception, please verify
			#-----------------------------------
			# if not (columns == set(columns) & set(query.getColumnsList(resultset))) :
			if not (columns == query.getColumnsList(resultset)) :
				Log.writeLog('query columns did not matched. query result : ' + str(resultset), strs.ERRO)
				db_con.close()
				continue
			#eof-debug-code


			#------------------------
			#-- upload | write to file
			#------------------------
			if self.generateReport(resultset) != strs.success :
				""" if any error entry
				"""
				Helpers.displayText('fetching report: completed with some error')
				Log.writeLog('fetching report: completed with some error', strs.INFO)

			Helpers.displayText('fetching report: completed')
			Log.writeLog('fetching report: completed', strs.INFO)
			

			# close connectin
			try:
				db_con.close()
			except Exception, e:
				pass

