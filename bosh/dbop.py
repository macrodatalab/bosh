import getpass

d_type = "postgresql"
d_host = "localhost"
d_port = ""
d_user = ""
d_pass = ""
d_db = ""

def append(line , bo_host , bo_port):
	import subprocess
	import os
	import signal
	from distutils.sysconfig import get_python_lib
	boshcwd =os.getcwd()
	lib_path = get_python_lib() 
	
	if line != "" and d_type == "mysql":
		mysql_ap = subprocess.Popen(["python", lib_path + "/db2bt/mysql2bt.py" , d_host , d_port, d_db , d_user ,d_pass, line, bo_host , str(bo_port), "append"])
		print("append" + d_type + " table " + line + " from db " + d_db + " at " + d_host + ":" + d_host + " to BigObject server " + bo_host + ":" + str(bo_port) ) 
		mysql_ap.wait()
		return
	elif line != "" and d_type == "postgresql":
		psql_ap = subprocess.Popen(["python", lib_path + "/db2bt/psql2bt.py" , d_host , d_port, d_db , d_user ,d_pass, line, bo_host , str(bo_port) , "append"])
		print("append" + d_type + " table " + line + " from db " + d_db + " at " + d_host + ":" + d_host + " to BigObject server " + bo_host + ":" + str(bo_port) ) 
		psql_ap.wait()
		return

def copy(line , bo_host , bo_port):
	import subprocess
	import os
	import signal
	from distutils.sysconfig import get_python_lib
	boshcwd =os.getcwd()
	lib_path = get_python_lib() 
	
	if line != "" and d_type == "mysql":
		mysql_cp = subprocess.Popen(["python", lib_path + "/db2bt/mysql2bt.py" , d_host , d_port, d_db , d_user ,d_pass, line, bo_host , str(bo_port)])
		print("copy" + d_type + " table " + line + " from db " + d_db + " at " + d_host + ":" + d_host + " to BigObject server " + bo_host + ":" + str(bo_port) ) 
		mysql_cp.wait()
		return
	elif line != "" and d_type == "postgresql":
		psql_cp = subprocess.Popen(["python", lib_path + "/db2bt/psql2bt.py" , d_host , d_port, d_db , d_user ,d_pass, line, bo_host , str(bo_port)])
		print("copy" + d_type + " table " + line + " from db " + d_db + " at " + d_host + ":" + d_host + " to BigObject server " + bo_host + ":" + str(bo_port) ) 
		psql_cp.wait()
		return

def showdb():
	print("db type:\t" + d_type + "\ndb name:\t" + d_db + "\nhost:\t\t" + d_host + ":" + d_port + "\nuser:\t\t" + d_user )

def setdb():
	global d_type, d_host, d_port, d_user, d_pass, d_db
	dbtype = raw_input(">>> database type [" + d_type + "] : " )
	if dbtype != "":
		d_type = dbtype
	host = raw_input(">>> host [" + d_host + "] : " )
	if host != "":
		d_host = host
	port = raw_input(">>> port [" + d_port + "] : " )
	if port != "":
		d_port = port
	username = raw_input(">>> username [" + d_user + "] : " )
	if username != "":
		d_user = username
	password = getpass.getpass(">>> Password (hidden) : ")
	if password != "":
		d_pass = password
	dbname = raw_input(">>> database name [" + d_db + "] : " )
	if dbname != "":
		d_db = dbname
