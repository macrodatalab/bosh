#!/usr/bin/python
# encoding=utf8  
import sys
from subprocess import Popen, PIPE
from rpcshell import cmd2JSON, json_stream
import rpcshell
import requests
import json

reload(sys)  
sys.setdefaultencoding('utf8')

def return_data(data_str , no_print=False):
	data = json.loads(data_str)
	#print(data)
	#count = 0
	return_str = ""

	if(type(data['Content']) != dict):
		if json.dumps(data['Content']) != "null":
			if data['Content'] != "":
				if no_print == False:
					print(json.dumps(data['Content'],ensure_ascii=False, indent=4))
				return_str = json.dumps(data['Content'])
		else:
			if data['Err']!= "":
				if no_print == False:
					print(json.dumps(data['Err'], indent=4))
				return_str = json.dumps(data['Err'])
		return return_str

	if 'content' in data['Content'].keys():
		for row in data['Content']['content']:
			#print("row :" ,row)
			print_row=""
			for record in row:
				if print_row != "":
					print_row += ","
                    		print_row += str(record).decode('utf-8')
				#print(print_row)
			if no_print == False:
				print(print_row)	
			
			if return_str != "":
				return_str += "\n"
			#print(return_str)
			return_str = return_str + print_row	
			#print("return_str : " ,return_str , " , print_row : " , print_row)
			#print(row)
			#count+=1
	else:
		if data['Content'] != "":
			if no_print == False:
				print(json.dumps(data['Content'], indent=4))
			return_str = json.dumps(data['Content'])
	#print(return_str)
	return return_str
 
def return_Data(server,cmdStr, no_print , workspace_name , timeout=9999):
	ret_str = ""
	r = requests.post(server,data=cmd2JSON(cmdStr, workspace_name) , stream=True , timeout=timeout)
	for content in json_stream(r.raw):
		if ret_str != "":
			ret_str += "\n"
		ret_str = ret_str + return_data(json.dumps(content) , no_print)
	return ret_str

def send_return(connargs, shell_name, command):
	bo_url = "http://" + connargs["host"] + ":" + str(connargs["port"]) + "/cmd"
	workspace_name = connargs["workspace"]
	cmd1 = command.split("\"")[1]
	cmd2 = command.split("\"")[3]
	ret_table = (command.split("\"")[4]).split(" ")[3]
	#print cmd1 
	#print cmd2
	#print ret_table
	sneder = Popen(cmd2, shell=True, stdin=PIPE, stdout=PIPE)	

	res = return_Data(bo_url , cmd1 , True , workspace_name , connargs["timeout"])
	#print res
	out, err = sneder.communicate(input=res)
	sneder.wait()

	insert_stmt = ""
	for line in out.split('\n'):
		#print "::::" , line.rstrip()
		if line != "":
			print line
		else:
			break
		if insert_stmt != "":
			insert_stmt = insert_stmt + ","

		if len(line.split()) == 0:
			insert_stmt = insert_stmt + "(\"" +  line + "\")"
		else:
			insert_stmt = insert_stmt + "(\"" + "\",\"".join([str(col) for col in line.split()]) + "\")"
		#print ",".join([str(col) for col in line.split()])
		#print ",".join([str(wtf) for wtf in p])

	insert_stmt = "INSERT INTO " + ret_table + " VALUES" + insert_stmt
	print rpcshell.shell(connargs, "" , insert_stmt)

def send(connargs, shell_name, command):
	bo_url = "http://" + connargs["host"] + ":" + str(connargs["port"]) + "/cmd"
	workspace_name = connargs["workspace"]
	cmd1 = command.split("\"")[1]
	cmd2 = command.split("\"")[3]
	sneder = Popen(cmd2, shell=True, stdin=PIPE)	
	
	#print "cmd1 : " , cmd1
	#print "cmd2 : " , cmd2
	res = return_Data(bo_url , cmd1 , True , workspace_name , connargs["timeout"])
	#print res
	sneder.communicate(input=res)
	sneder.wait()

def receive(connargs, shell_name, command):
	bo_url = "http://" + connargs["host"] + ":" + str(connargs["port"]) + "/cmd"
	workspace_name = connargs["workspace"]
	cmd1 = command.split("\"")[0].split(" ")[0]
	cmd2 = command.split("\"")[1]
	#print "cmd1 :" , cmd1
	#print "cmd2 :" , cmd2
	proc = Popen(cmd2, shell=True ,stdout=PIPE)
	insert_stmt = ""
	for line in iter(proc.stdout.readline,''):
		#print "::::" , line.rstrip()
		print line.strip()
		if insert_stmt != "":
			insert_stmt = insert_stmt + ","

		if len(line.split()) == 0:
			insert_stmt = insert_stmt + "(\"" +  line + "\")"
		else:
			insert_stmt = insert_stmt + "(\"" + "\",\"".join([str(col) for col in line.split()]) + "\")"
		#print ",".join([str(wtf) for wtf in p])

	insert_stmt = "INSERT INTO " + cmd1 + " VALUES" + insert_stmt
	print rpcshell.shell(connargs, "" , insert_stmt)
	#print insert_stmt	

if __name__ == "__main__":
        #cmd = sys.argv[1]
	#connargs={}
	#connargs["host"] = "localhost"
	#connargs["port"] = 9090
	#connargs["timeout"] = 9999
	#connargs["workspace"]= ""
	#connargs["opts"]=""
	#send(connargs , "" , cmd )
	#receive(connargs , "" , cmd)
	#send_return(connargs , "" , cmd )
	print "all done"
