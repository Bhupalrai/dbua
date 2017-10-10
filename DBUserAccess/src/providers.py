"""
All object providers are implemented here
"""

import strs
from logs import Log
from databases import OracleDatabase
from databases import VerticaDatabase
from databases import MssqlDatabase

class DatabaseProvider(object):
	"""
	Database class provider
	"""
	def getDatabase(self, db_type):

		if db_type == strs.db_type_oracle:
			oracle_db_obj = OracleDatabase()
			if oracle_db_obj :
				return oracle_db_obj

		if db_type == strs.db_type_vertica:
			vertica_db_obj = VerticaDatabase() 
		 	if vertica_db_obj :
		 		return vertica_db_obj

		if db_type == strs.db_type_mssql:
			mssql_db_obj = MssqlDatabase() 
			if mssql_db_obj :
				return mssql_db_obj

		# return 0 for not vailable or error on creating objects
		return 0