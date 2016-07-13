# encoding=utf8  
import requests
import json
import sys
import time

reload(sys)  
sys.setdefaultencoding('utf8')


def cmd2JSON(cmd , workspace_name=""):
	return json.dumps({'Stmt':cmd,'Workspace':workspace_name,'Opts':{}})

def getData(server,cmdStr,show_total_count , workspace_name , timeout=9999):
	r = requests.post(server,data=cmd2JSON(cmdStr, workspace_name) , stream=True , timeout=timeout)
	#print(r)
	total_row = 0
	check_save = True
	for content in json_stream(r.raw):
		total_row += printdata(json.dumps(content))
		if(check_save == True and total_row > 1000):
			check_save = resDataSave(server, cmdStr)
			if check_save == True:
				show_total_count = False
				break				

	if show_total_count == True :
		print("=============\ntotal row : " + str(total_row))	

def json_stream(fp):
	for line in fp:
		#print(line)
		yield json.loads(line)

def resDataSave(bo_url , cmdstr , passQ = False , dumptype='CSV', dump_filename='dump.csv'):
	if passQ == False:
		confirmStr= "=============\nSize of data exceeded display limit, dump to csv format? (yes/no)"
		import fileinput
		print confirmStr
		while True:
			choice=raw_input()
		        if choice=="yes" or choice=="y":
			        break
		        elif choice=="no" or choice=="n":
				return False
			else:
				print confirmStr
	#bo_host = bo_url.split(":")[1][2:]
	#bo_port = bo_url.split(":")[2][:-4]
	import subprocess
	import os
	import signal
	from distutils.sysconfig import get_python_lib
	boshcwd =os.getcwd()
	lib_path = get_python_lib() 

	rest = subprocess.Popen(["python", lib_path + "/dumpRes/borestful.py" , bo_url , cmdstr ], stdout=subprocess.PIPE)
	tocsv = subprocess.Popen(["python", lib_path + "/dumpRes/bojson2file.py", dumptype, boshcwd + "/" + dump_filename] , stdin=rest.stdout)
	print("dumping the data to " + dump_filename + " , type: " + dumptype + " ...")
	rest.wait()
	tocsv.wait()
	return True

def printdata(data_str):
	data = json.loads(data_str)
	count = 0
	if(type(data['Content']) != dict):
		if json.dumps(data['Content']) != "null":
			if data['Content'] != "":
				print(json.dumps(data['Content'], indent=4))
		else:
			if data['Err']!= "":
				print(json.dumps(data['Err'], indent=4))
		return 0	

	if 'content' in data['Content'].keys():
		for row in data['Content']['content']:
			#print(row)
			print_row=""
			for record in row:
				if print_row != "":
					print_row += ","
                    		print_row += str(record).decode('utf-8')
			print(print_row)		
			#print(row)
			count+=1
	else:
		if data['Content'] != "":
			print(json.dumps(data['Content'],ensure_ascii=False, indent=4))
	
	return count
 
def shell(connargs, shell_name, command, show_total_count=False):
	bo_url = "http://" + connargs["host"] + ":" + str(connargs["port"]) + "/cmd"
	workspace_name = connargs["workspace"]
	now = time.time()
	if command.find(">>>") > 0 and command[:7] != "INSERT " and command[:7] != "insert ":
		real_cmd = command.split(">>>")[0].strip()
		dump_name = command.split(">>>")[1].strip()
		dump_type = 'CSV';
		#print(real_cmd , " ||| " , dump_name)
		if dump_name.find(".xlsx") > 0 or dump_name.find(".XLSX") > 0:
			dump_type = 'XLSX'
		resDataSave(bo_url , real_cmd , True, dump_type , dump_name)
	else:
		getData(bo_url, command, show_total_count , workspace_name , connargs["timeout"]) 
	end = time.time()
	print '-- execution time: %ss' %  str(round((end - now),2))
	


def return_getData(server,cmdStr, no_print , workspace_name , timeout=9999):
	ret_str = ""
	r = requests.post(server,data=cmd2JSON(cmdStr, workspace_name) , stream=True , timeout=timeout)
	for content in json_stream(r.raw):
		if ret_str != "":
			ret_str += ","
		ret_str = ret_str + return_printdata(json.dumps(content) , no_print)
	#print("ret_str")
	#print(ret_str )
	return ret_str
	
def return_printdata(data_str , no_print=False):
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
				#if print_row != "":
				#	print_row += ","
                    		print_row += str(record).decode('utf-8')
				#print(print_row)
			if no_print == False:
				print(print_row)	
			
			if return_str != "":
				return_str += ","
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
 

def shell_return(connargs, shell_name, command, no_print=False):
	bo_url = "http://" + connargs["host"] + ":" + str(connargs["port"]) + "/cmd"
	workspace_name = connargs["workspace"]
	now = time.time()
	temp = return_getData(bo_url, command, no_print , workspace_name , connargs["timeout"]) 
	#print("temp")
	#print(temp)
	end = time.time()
	if no_print == False:
		print '-- execution time: %ss' %  str(round((end - now),2))
	return temp


if __name__ == "__main__":
	connargs={}
	connargs["host"] = "localhost"
	connargs["port"] = "9090"
	shell(connargs, "*" ,"select * from sales limit 10")

