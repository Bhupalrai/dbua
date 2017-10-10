"""
All actions involving database is implemented here
"""

import cx_Oracle
import pyodbc
from abc import ABCMeta, abstractmethod

import strs
from logs import Log


class Database( object ) :
	"""
	Database related task are implemented here within modules
	"""

	__metaclass__ = ABCMeta

	
	@abstractmethod
	def getDbConnection(self, db_access_dict):
		"""
		Abstract method to get database connection
		"""
		pass

	def closeDbConnection(self, db_conn):
		"""
		Implemetation of closing database connection task
		"""
		try:
			db_conn.close()
			return True

		except Exception, e:
			Log.writeLog('Exception while closing connection', strs.ERRO)
			return False




class VerticaDatabase(Database) :
	"""
	Implements Databse class for vertica 
	"""	

	db_conn = None

	def getDbConnection (self, db_access_dict):
		"""
		Connect to vertica database
		"""

		try:
			conn_str = 'DRIVER={0:s}; SERVER={1:s}; DATABASE={2:s}; UID={3:s}; PWD={4:s};'.format( \
				strs.vertica_driver, \
				db_access_dict['server_name'], \
				db_access_dict['database_name'], \
				db_access_dict['user_name'], \
				db_access_dict['password'])
			self.db_conn = pyodbc.connect(conn_str)
			return self.db_conn

		except Exception, e:
			Log.writeLog('Exception while connecting to Database {0:s}'.format( \
				db_access_dict['database_name'] +'@'+ db_access_dict['server_name'] + 'Msg : '+ str(e)), strs.ERRO)
			return 0




class OracleDatabase(Database) :
	"""
	Implements Database class for oracle
	"""
	
	db_conn = None

	def getDbConnection(self, db_access_dict):
		"""
		Connect to vertica database
		"""

		try:
			conn_str = '{0:s}/{1:s}@{2:s}:{3:s}/{4:s}'.format( \
				db_access_dict['user_name'], \
				db_access_dict['password'], \
				db_access_dict['server_name'], \
				db_access_dict['port'], \
				db_access_dict['sid'])
			
			self.db_conn = cx_Oracle.connect(conn_str)
			return self.db_conn

		except Exception, e:
			Log.writeLog('Exception while connecting to Database {0:s}. Msg : {1:s}'.format( \
				db_access_dict['sid'] +'@'+ db_access_dict['server_name'], str(e)), strs.ERRO)
			return 0




class MssqlDatabase(Database) :
	"""
	Implements Database class for mssql
	"""
	
	db_conn = None

	def getDbConnection(self, db_access_dict):
		"""
		Connect to mssql database
		"""

		try:
			conn_str = "Driver={0:s};Server={1:s}; Database={2:s};UID={3:s};PWD={4:s}".format( \
				strs.mssql_driver , \
				db_access_dict['server_name'] + ',' + db_access_dict['port'], \
				db_access_dict['database_name'], \
				db_access_dict['user_name'], \
				db_access_dict['password'])
			self.db_conn = pyodbc.connect(conn_str)
			return self.db_conn

		except Exception, e:
			Log.writeLog('Exception while connecting to Database {0:s}. Msg : {1:s} '.format( \
				db_access_dict['database_name'] +'@'+ db_access_dict['server_name'], str(e)), strs.ERRO)
			return 0


