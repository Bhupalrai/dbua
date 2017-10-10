"""
Implements information uploading to database tasks
"""
import strs
from logs import Log
from helpers import Helpers
from configuration import ConfigReader
from providers import DatabaseProvider

class Upload(object):

	def uploadOutput(self, input_list = None, input_resulset = None, table_name = None):
		"""
		Uploads the input_list, input_resulset to the target table.
		If input_list is empty, uploads insert_string else uploads input_list

		rtype: success 
		"""

		self.error_count = 0

		
		self.input_list = input_list
		self.input_resulset = input_resulset		
		self.table_name = table_name


		# get meta server connection
		meta_svr_con_para_dict =  ConfigReader.getMetaSvrAccessPara()
		database_provider = DatabaseProvider()
		metaserver_db_obj = database_provider.getDatabase(strs.metaserver_db_type)
		if not metaserver_db_obj :
			Log.writeLog('meta server object creating failed', strs.ERRO)
			raise SystemExit('meta server object creating failed')

		# decrypt password
		meta_svr_con_para_dict['password'] = Helpers.scramblePwd(strs.decrypt, '', meta_svr_con_para_dict['password'])
		meta_svr_con = metaserver_db_obj.getDbConnection(meta_svr_con_para_dict)	
		if not meta_svr_con : 
			Log.writeLog('meta server database connection failed', strs.ERRO)			
			raise SystemExit('meta server database connection failed.')
		
		# upload
		if input_list :
			return self.uploadList(meta_svr_con, input_list)
		elif input_resulset :
			return self.uploadResultset(meta_svr_con, input_resulset)
		else:
			return None




	def uploadResultset(self, db_con, input_resulset):
		"""
		Upload the resultset here
		"""
		cursor = db_con.cursor()
		columns = []
		columns = Helpers.getColumnList(input_resulset)

		error_count = 0

		for record in input_resulset:
			insert_string = strs.insert_query_to_dbua_audit_report_table.format(record[0],record[1],record[2],record[3], record[4], record[5])			
			#Log.writeLog(insert_string, strs.INFO)
			try:
				cursor.execute(insert_string)
				db_con.commit()
			except Exception, e:
				Log.writeLog('Error in executing : ' + insert_string +' Msgs : ' + str(e), strs.ERRO)
				Helpers.writeToFile(strs.invalid_entries_csv, '|'.join(map(str, record)) )
				error_count = error_count + 1

		db_con.close()
		return error_count



	def uploadList(self, db_con, input_list):
		"""
		Upload list here
		"""
		pass
		# error_count = 0

		# # INSERT INTO DBUA_AUDIT_REPORT VALUES(DBUA_AUDIT_REPORT_SEQ.NEXTVAL, 'TEST_SERVER_NAME','TEST_DATABASE','TEST_USER','TEST_PREV');
		# cursor = db_con.cursor()
		# for rec in self.input_list:
		# 	for record in rec:
		# 		insert_string = strs.insert_query_to_dbua_audit_report_table.format(record[0],record[1],record[2],record[3], record[4])
				
		# 		#Log.writeLog(insert_string, strs.INFO)
		# 		try:
		# 			cursor.execute(insert_string)
		# 			self.db_con.commit()					
		# 		except Exception, e:
		# 			Log.writeLog('Error in uploqeing the record : ' + str(record) +' Msgs : ' + str(e), strs.ERRO)
		# 			error_count = error_count + 1
		# return error_count


