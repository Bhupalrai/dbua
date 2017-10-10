#------------------------------------------------------------------------------------------------------------------
#----STRING VARIABLES
#------------------------------------------------------------------------------------------------------------------



#
# debug strings
#
getting_storage_cred = 'getting credidentals for storage'
getting_backup_cred = 'getting credidentals for backupSvrSetup'



#
# Database
#
db_conn_failed = 'Database Connection Failed'
db_conn_success = 'Database Connection Successful'
strGtCon = 'getting database connection'




#
# database type
#
db_type_oracle = 'oracle'
db_type_vertica = 'vertica'
db_type_mssql = 'mssql'




#
# Metaserver database type
#
metaserver_db_type = db_type_oracle

#
# Drivers
#
vertica_driver = 'HPVertica'
mssql_driver='MSSQLServer'



#
# success/failure
#
success = 'success'
failure = 'failure'



#
# Log category
#
INFO = 'INFO'
WARN = 'WARN'
ERRO = 'ERRO'
DEBG = 'DEBG'

log_level_high  = '2'
log_level_debug = '1'
log_level_min   = '0'


log_file_name = 'dbuseraccess.log'



#
# configuration file
#
meta_svr_conf_file = './conf/metaserver-conf.cfg'
meta_svr_conf_file_section_meta_svr_conf = 'meta-svr-conf'

dbu_conf_file = './conf/dbu-conf.cfg'
dbu_conf_file_section_dbu_log = 'dbu-log'




#
# dump / output file formates
#
output_formate_csv = 'output_to_csv'
output_formate_excel = 'output_to_excel"'
output_file_csv = './output/output.csv'
invalid_entries_csv = './output/invalid_entries.csv'
output_file_excel = './output/output.xls'



#
# encryption
#
encrypt = 'enc'
decrypt = 'drc'


#
# query
#

insert_query_to_dbua_audit_report_table = 'INSERT INTO DBUA_AUDIT_REPORT (id, servername, database, username, privilegs_and_roles, login_type, audit_date, database_type ) \
                  VALUES(DBUA_AUDIT_REPORT_SEQ.NEXTVAL,\'{0:s}\', \'{1:s}\', \'{2:s}\', \'{3:s}\', \'{4:s}\', sysdate, \'{5:s}\')'

global_query = """
SELECT 
T_DBUA_DB_TYPE_DBUA_QUERY.DATABASE_TYPE,    
T_DBUA_DB_TYPE_DBUA_QUERY.QUERY,  
T_DBUA_INVENTRY.SERVER,
T_DBUA_INVENTRY.DATABASE_NAME,
T_DBUA_INVENTRY.PORT,
T_DBUA_INVENTRY.SID,
T_DBUA_INVENTRY.USERID,
T_DBUA_INVENTRY.PWD
FROM 
  (
    SELECT 
    T_DBUA_DB_TYPE.DB_TYPE_ID,
    T_DBUA_DB_TYPE.DATABASE_TYPE,
    T_DBUA_DB_TYPE.DESCRIPTION, 
    T_DBUA_QUERY.QUERY  
    FROM
      ( SELECT DB_TYPE_ID, DATABASE_TYPE, DESCRIPTION FROM  DBUA_DB_TYPE
		) T_DBUA_DB_TYPE
      INNER JOIN 
      ( SELECT DB_TYPE_ID, QUERY FROM  DBUA_QUERY
		) T_DBUA_QUERY

      ON T_DBUA_DB_TYPE.db_type_id = T_DBUA_QUERY.db_type_id
  ) T_DBUA_DB_TYPE_DBUA_QUERY    
  INNER JOIN 
  (
    SELECT * FROM  DBUA_INVENTRY
  ) T_DBUA_INVENTRY   
ON T_DBUA_DB_TYPE_DBUA_QUERY.DB_TYPE_ID = T_DBUA_INVENTRY.DB_TYPE_ID
"""


#
# mssql specific query
#
sql_inventry_proc = 'sql_inventry'
drop_inventry_if_exists = \
"if exists (SELECT *  FROM master.dbo.sysobjects WHERE name='sql_inventry' and type='P') \
begin \
use master;drop proc dbo.sql_inventry \
end"

create_mssql_proc_inventry ="""
create procedure sql_inventry(@BTYPE varchar(50))
 as
 begin
 IF EXISTS (SELECT 1 
  FROM INFORMATION_SCHEMA.TABLES 
   WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME='dbuser')
   begin
 drop table dbuser
 end
 DECLARE @DB_USers TABLE(DBName sysname, UserName sysname, LoginType sysname, AssociatedRole varchar(max),create_date datetime,modify_date datetime)
 INSERT @DB_USers EXEC sp_MSforeachdb
 'use [?]
 SELECT ''?'' AS DB_Name,
 case prin.name when ''dbo'' then prin.name + '' (''+ (select SUSER_SNAME(owner_sid) from master.sys.databases where name =''?'') + '')'' else prin.name end AS UserName,
 prin.type_desc AS LoginType,
 isnull(USER_NAME(mem.role_principal_id),'''') AS AssociatedRole ,create_date,modify_date
 FROM sys.database_principals prin
 LEFT OUTER JOIN sys.database_role_members mem ON prin.principal_id=mem.member_principal_id
 WHERE prin.sid IS NOT NULL and prin.sid NOT IN (0x00) and
 prin.is_fixed_role <> 1 AND prin.name NOT LIKE ''##%'''
 SELECT @@servername as servername, dbname,username ,STUFF((
 SELECT ',' + CONVERT(VARCHAR(500),associatedrole)FROM @DB_USers user2
 WHERE user1.DBName=user2.DBName AND user1.UserName=user2.UserName
 FOR XML PATH('')),1,1,'') AS Permissions_user,logintype into master.dbo.dbuser 
 FROM @DB_USers user1 GROUP BY 
 dbname,username ,logintype ,create_date ,modify_date ORDER BY DBName,username 
 end"""

execute_inventry = "exec sql_inventry 'asd' "
drop_inventry = 'drop procedure sql_inventry'