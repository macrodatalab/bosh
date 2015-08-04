import requests
import json
import sys
import time


def cmd2JSON(cmd):
	return json.dumps({'Stmt':cmd,'Workspace':"",'Opts':{}})

def getData(server,cmdStr,show_total_count):
	r = requests.post(server,data=cmd2JSON(cmdStr) , stream=True)
	#print(r.raw)
	#print("*************************")
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
		print("total row : " + str(total_row))	

def json_stream(fp):
	for line in fp:
		#print(line)
		yield json.loads(line)

def resDataSave(bo_url , cmdstr):
	confirmStr= "Size of data exceeded display limit, dump to csv format? (yes/no)"
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
	tocsv = subprocess.Popen(["python", lib_path + "/dumpRes/bojson2file.py", "CSV", boshcwd + "/dump.csv"] , stdin=rest.stdout)
	print("dumping the data to dump.csv...")
	rest.wait()
	tocsv.wait()
	return True

def printdata(data_str):
	data = json.loads(data_str)
	#print(data , type(data))
	#print(data['Content'] , type(data['Content']))
	count = 0
	if(type(data['Content']) != dict):
		#print("no return table can be dumpped, admin statement?")
		#print("data:\n" + str(data['Content']))
		#print(str(data['Content']))
		if json.dumps(data['Content']) != "null":
			print(json.dumps(data['Content'], indent=4))
		else:
			print(json.dumps(data['Err'], indent=4))
		return 0	

	if 'content' in data['Content'].keys():
		for row in data['Content']['content']:
			print(row)
			#print(json.dumps(row))
			#output.writerow(row)
			count+=1
	else:
		#print(str(data['Content']))
		print(json.dumps(data['Content'], indent=4))
		#print("no content can be dumpped, admin statement?")
		#print("data:\n" + str(data['Content']))
		
	return count
 
def shell(connargs, shell_name, command, show_total_count=False):
	bo_url = "http://" + connargs["host"] + ":" + str(connargs["port"]) + "/cmd"
	print("bourl: " + bo_url)
	now = time.time()
	getData(bo_url, command, show_total_count) 
	end = time.time()
	print 'execution time: %ss' %  str(round((end - now),2))
	
if __name__ == "__main__":
	connargs={}
	connargs["host"] = "localhost"
	connargs["port"] = "9090"
	shell(connargs, "*" ,"select * from sales limit 10")

