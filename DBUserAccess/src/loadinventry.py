import csv
import cx_Oracle
import sys
import ConfigParser
from databases import OracleDatabase
from helpers import Helpers
import strs

def loadData() :
	# read configuration. 
	config = ConfigParser.ConfigParser()
	config.read(strs.meta_svr_conf_file)
	access_para_dict = {}
	try:    
	    for item in config.options(strs.meta_svr_conf_file_section_meta_svr_conf):
	        access_para_dict[item] = config.get(strs.meta_svr_conf_file_section_meta_svr_conf, item)    
	except Exception, e:
		print str(e)
		raise SystemExit('Error parsing file:  '+ strs.meta_svr_conf_file_section_meta_svr_conf + '.' \
		+ ' Msg : ' + str(e) )

	
	access_para_dict['password'] = Helpers.scramblePwd(strs.decrypt, '', access_para_dict['password'])
	metaserver_db_obj = OracleDatabase()
	meta_svr_con = metaserver_db_obj.getDbConnection(access_para_dict)

	csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

	insert_string = "INSERT INTO UTILITY.DBUA_INVENTRY (INVENTRY_ID, SERVER, DB_TYPE_ID, DATABASE_NAME, PORT, SID, USERID, PWD) \
					VALUES( \
						DBUA_INVENTRY_SEQ.NEXTVAL, \
						'{0:s}', \
						'{1:s}', \
						'{2:s}', \
						'{3:s}', \
						'{4:s}', \
						'{5:s}', \
						'{6:s}' \
						)"
	
	cursor = meta_svr_con.cursor()
	error_count = 0
	with open('./bin/inventry_data.txt', "rb") as csvfile:		
		for row in csv.DictReader(csvfile, dialect='piper'):
			STR = insert_string.format( str(row['SERVERIP']), \
				  str(row['DB_TYPE_ID']).strip(), \
				  str(row['DATABASE_NAME']).strip(), \
				  str(row['PORT']).strip(), \
				  str(row['SID']).strip(), \
				  str(row['USERID']).strip(), \
				  getPlainPwd(str(row['PWD']) ).strip())
			try:
				cursor.execute(STR)
				meta_svr_con.commit()
			except Exception, e:
				print 'Error while uploading : Msg: ' + str(e)+ str(row) 
				error_count = +1
	return error_count


def getPlainPwd( encrypted_pwd ):
	from random import randint
	import subprocess
	import shlex

	random_seed = randint(1000000000, 9999999999)
	plain_pwd = None
	try:
		plain_pwd = str(encrypted_pwd)
	except Exception, e:
		raise SystemExit('Error in password argument field. Argument value: '+ str(plain_pwd))
	if not plain_pwd :
		raise SystemExit('Error in password argument field. Argument value: '+ str(plain_pwd))

	cmd_string = './bin/scramble.out "{0:s}" "{1:s}" "{2:s}"'.format(plain_pwd.strip(),"   ", str(random_seed))
	
	scramble_cmd = subprocess.Popen(shlex.split(cmd_string), stdout=subprocess.PIPE)
	for line in scramble_cmd.stdout:
		scramble_pwd = str(line)
		scramble_cmd.communicate()
		return scramble_pwd.replace('\n', '').strip()
		
		