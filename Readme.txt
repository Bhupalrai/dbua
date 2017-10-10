DBUserAccess 1.0.0_f0
A python application to collect the user access privilege in a database.



Requirements:
-------------

1. python 2.6.8
2. pyodbc 3.0.3
3. unixODBC 2.3.0 ( configure for vertica/mssql)
3. cx_Oracle 5.1.3
4. Create folder to write log and give read/write permission to user running the application. The folder

Patch to apply:
1. p_100 on metadata server


How to run:
-----------
1. $ cd DBUserAccess x.x.x/DBUserAccess
2. make scramble.out file located at /bin folder executable.
   $ chmod +x bin/scramble.out
3. $ python2.6 DBUserAccess.py



Generate password:
------------------
1. change directory to bin/ folder
2. make scramble.out file located at /bin folder executable.
3. run command: $ python2.6 python2.6 generate_pwd.py "<plain-password-here>"
   e.g. to encrypt 'test-password'
        $ python2.6 generate_pwd.py



Note:
---------------
Configuring unixODBC for vertica
--------------------------------
install vertica client.rpm
edit /etc/odbcinst.ini create Vertica Driver entry "HPVertica"


