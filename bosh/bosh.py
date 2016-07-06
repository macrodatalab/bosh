import sys
import cmd
import os
import rpcshell
import re
import csvloader
from urlparse import urlparse
import tools
#import getpass
import traceback
import dbop

class adminCmd(cmd.Cmd):
    adminword = [ 'luaupload' , 'LUAUPLOAD', 'CSVLOADER' , 'csvloader']
    def completedefault(self, text, line, begidx, endidx):
        if not text:
            completions = self.adminword[:]
        else:
            completions = [ f
            for f in self.adminword
            if f.startswith(text)
            ]
        return completions
    def emptyline(self):
        pass
    def do_EXIT(self, line):
        return True
    def do_exit(self, line):
        return True
    def do_EOF(self, line):
        return True
    def do_QUIT(self, line):
        return True
    def do_quit(self, line):
        return True
    def do_LS(self,line):
	self.do_ls(line)
    def do_ls(self,line):
	print '\n'.join(str(p) for p in os.listdir(".")) 
    def do_LUAUPLOAD(self, line):
	self.do_luaupload(line)
    def do_luaupload(self, line):
	import requests
	if line != "":
		#print(line)
		try:
			payload = open(line, 'rb')
			server = 'http://' + self.connargs["host"] + ":" + str(self.connargs["port"]) + "/script/" + line
		        r = requests.post(server, data=payload, headers={'Content-Type':'application/x-www-form-urlencoded'})
			print(r.text)	
		except IOError:
		        print ('cannot open file \"' + line + '\"')
	else:
		print("luaupload <lua file name>")
	
    def do_sethost(self, line):
        if line != "":
            self.connargs["host"] = line
    def do_setport(self, line):
        if line != "":
            self.connargs["port"] = line
    def do_settimeout(self, line):
        if line != "":
            self.connargs["timeout"] = line
    def do_CSVLOADER(self, line):
        self.do_csvloader(line)
    def do_csvloader(self, line):
        if line != "":
            input_line = line.split();
            if len(input_line) >= 2:
		row_size_in_a_stmt = 30000
		noncheck_mod = False
		if len(input_line) >= 3 and input_line[2] == 'boost':
			noncheck_mod = True
			if len(input_line) == 4:
				row_size_in_a_stmt = int(input_line[3])
		elif len(input_line) == 3 and input_line[2] != 'boost': 			
			row_size_in_a_stmt = int(input_line[2])
		else:
			noncheck_mod = False
			
                print csvloader.csvload(self.connargs, input_line[0] , input_line[1] , row_size_in_a_stmt , noncheck_mod)
            else:
                print "csvloader <csv_file> <bt_name>"
    def do_info(self, line):
        print "host : " + self.connargs["host"]
        print "port : " + str(self.connargs["port"])
        print "workspace : " + self.connargs["workspace"]
        print "timeout : " + str(self.connargs["timeout"])

    def help_psql(self):
        print "\trun postgresql client. psql required"
    def help_csvloader(self):
        print "\tload a local CSV file into a server-side BigObject table\n\tex. csvloader <csv_file> <bt_name>"
    def help_sethost(self):
        print "\tset host name"
    def help_setport(self):
        print "\tset port"
    def help_settimeout(self):
        print "\tset timeout value"

class baseCmd(cmd.Cmd):
    assocword = [ 'create' , 'find', 'select' , 'build' , 'use' , 'apply' , 'get' ,'insert' , 'update' , 'alter', 'association', 'from' , 'by' , 'where' , 'query' , 'tables' , 'from', 'by', 'group by' , 'where' , 'tree' , 'table' , 'workspace' , "send" , "receive" ]
    def completedefault(self, text, line, begidx, endidx):
        if not text:
	    #print(text , line)
            completions = self.assocword[:]
        else:
            #print(text , line)
            completions = [ f
            for f in self.assocword
            if f.startswith(text)
            ]
	#print(completions)
        return completions


    def __init__(self):
        cmd.Cmd.__init__(self)
        try:
            import readline
            readline.set_history_length(80)
            try:
                readline.read_history_file()
            except IOError:
                readline.write_history_file()
        except ImportError:
            try :
                import pyreadline as readline
                readline.set_history_length(80)
                try:
                    readline.read_history_file()
                except IOError:
                    readline.write_history_file()
            except ImportError:
                pass

    ############# BigObject ##############
    def do_CREATE(self, line):
        self.do_create(line)
    def do_create(self, line):
        print rpcshell.shell(self.connargs, "" , "create " + line)
    def do_BUILD(self, line):
        self.do_build(line)
    def do_build(self, line):
        rpcshell.shell(self.connargs, "" , "build " + line)
    def do_SHOW(self,line):
        self.do_show(line)
    def do_show(self, line):
	#print self.assocword
	#rpcshell.shell(self.connargs, "","show " + line)
	if line.strip() == 'tables' or line.strip() == 'tree':
		return_var = rpcshell.shell_return(self.connargs, "","show " + line)
		#print(return_var)
		#list1 = re.split(', ',return_var[1:-1].replace('"', ""))
		list1 = re.split(',',return_var.replace('"', ""))
		for l_e in list1:
			#print("l_e : " )
			#print(l_e )
			if not l_e in self.assocword:
				self.assocword.append(str(l_e))
		#print self.assocword
		
	else:
		rpcshell.shell(self.connargs, "","show " + line)

    def do_DESC(self, line):
        self.do_desc(line)
    def do_desc(self, line):
	rpcshell.shell(self.connargs, "","desc " + line)
    def do_FIND(self,line):
        self.do_find(line)
    def do_find(self, line):
        rpcshell.shell(self.connargs, "" , "find " + line , True)
    def do_APPLY(self,line):
        self.do_apply(line)
    def do_apply(self, line):
        rpcshell.shell(self.connargs, "" , "apply " + line , True)
    def do_SET(self,line):
        self.do_set(line)
    def do_set(self,line):
        rpcshell.shell(self.connargs, "" , "set " + line)  
    def do_GET(self,line):
        self.do_get(line)
    def do_get(self, line):
        rpcshell.shell(self.connargs, "" , "get " + line , True)  
    def do_TRIM(self,line):
        self.do_trim(line)
    def do_trim(self, line):
        rpcshell.shell(self.connargs, "" , "trim " + line)
    def do_SELECT(self, line):
        self.do_select(line)
    def do_select(self, line):
        rpcshell.shell(self.connargs, "" , "select " + line , True)

    def do_SEND(self, line):
        self.do_send(line)
    def do_send(self, line):
        rpcshell.shell(self.connargs, "" , "send " + line)

    def do_RECEIVE(self, line):
        self.do_receive(line)
    def do_receive(self, line):
        rpcshell.shell(self.connargs, "" , "receive " + line)



    def do_DELETE(self, line):
        self.do_delete(line)
    def do_delete(self, line):
        rpcshell.shell(self.connargs, "" , "delete " + line)

    def do_SUSPEND(self, line):
        self.do_suspend(line)
    def do_suspend(self, line):
        rpcshell.shell(self.connargs, "" , "suspend " + line)

    def do_RESUME(self, line):
        self.do_resume(line)
    def do_resume(self, line):
        rpcshell.resume(self.connargs, "" , "resume " + line)

    def do_INSERT(self, line):
        self.do_insert(line)
    def do_insert(self, line):
        if line != "":
            print rpcshell.shell(self.connargs, "" , "insert " + line)
    def do_UPDATE(self, line):
        self.do_update(line)
    def do_update(self, line):
        if line != "":
            print rpcshell.shell(self.connargs, "" , "update " + line)
    def do_ALTER(self, line):
        self.do_alter(line)
    def do_alter(self, line):
        if line != "":
            print rpcshell.shell(self.connargs, "" , "alter " + line)       

    def do_USE(self,line):
        self.do_use(line)
    def do_use(self,line):
        cmdSplits=line.split()
        if cmdSplits[0] != "workspace":
		wsStr=cmdSplits[0]
		self.connargs["workspace"]=cmdSplits[0]
	else:
	        wsStr=cmdSplits[1] if len(cmdSplits) > 1 else ""
	        if wsStr=="default" or wsStr=="":
	            self.connargs["workspace"]=""
	       	    #rpcshell.shell(self.connargs, "" , "use workspace default")
	        else:
	            self.connargs["workspace"]=wsStr
	            #sqlStr="create workspace "+wsStr
		    #rpcshell.shell(self.connargs, "" , "use " + line)
        print "switch to workspace:" +str(wsStr)

    def do_DROP(self,line):
        self.do_drop(line)
    def do_drop(self, line):
	cmdSplits=line.split()
        if cmdSplits[0] == "workspace":
	        wsStr=cmdSplits[1] if len(cmdSplits) > 1 else ""
	        if wsStr=="":
	            print("usage: drop workspace <workspace_name>")
	        else:
	            rpcshell.shell(self.connargs, "" , "drop " + line)
	            self.connargs["workspace"]=""
	        print "switch to default workspace"
	else:
	        rpcshell.shell(self.connargs, "" , "drop " + line)

    ##################### bosh ###########################
    def init_complete(self):
	tmp_timeout = self.connargs["timeout"]
	self.connargs["timeout"]=1
	try:
		#print self.assocword
		return_var = rpcshell.shell_return(self.connargs, "","show tables" , True)
		list1 = re.split(',',return_var.replace('"', ""))
		for l_e in list1:
			if not l_e in self.assocword and l_e != '':
				self.assocword.append(str(l_e))
		return_var = rpcshell.shell_return(self.connargs, "","show tree" , True)
		list1 = re.split(',',return_var.replace('"', ""))
		for l_e in list1:
			if not l_e in self.assocword and l_e != '':
				self.assocword.append(str(l_e))
		#print self.assocword

		#return_var = rpcshell.shell_return(self.connargs, "","show tables" , True)
		#list_table = re.split(', ',return_var[1:-1].replace('"', ""))
		#for tab1 in list_table:
		#	if not tab1 in self.assocword:
		#		self.assocword.append(tab1)

		#return_var = rpcshell.shell_return(self.connargs, "","show tree" , True)
		#list_tree = re.split(', ',return_var[1:-1].replace('"', ""))
		#for tree1 in list_tree:
		#	if not tree1 in self.assocword:
		#		self.assocword.append(tree1)
	except:
		print("\n\n==========================================================" )
		print("= Connection Error, please check host and port setting.  =" )
		print("==========================================================" )

	self.connargs["timeout"]=tmp_timeout
    def do_EXIT(self, line):
        return True
    def do_exit(self, line):
        return True
    def do_EOF(self, line):
        return True
    def do_QUIT(self, line):
        return True
    def do_quit(self, line):
        return True
    def emptyline(self):
        pass
    def do_INFO(self, line):
        self.do_info(line)
    def do_info(self, line):
        print "host : " + self.connargs["host"]
        print "port : " + str(self.connargs["port"])
        print "workspace : " + self.connargs["workspace"]
	print "timeout : " + str(self.connargs["timeout"])

    def do_ADMIN(self, line):
        self.do_admin(line)
    def do_admin(self, line):
        newcmd = adminCmd()
        newcmd.connargs = self.connargs
        newcmd.prompt = self.prompt[:len(self.prompt)-1] + ":admin>"
        newcmd.cmdloop()
    def do_PRINT(self,line):
        self.do_print(line)
    def do_print(self,line):
        command=line.split(">>")
        if len(command)==2:
            doInvoke=False
            outfile=str()
            if "@" in command[1]:
                outfile=command[1][command[1].find("@")+1:].strip()
                if len(outfile)==0:
                    return "*** FILENAME required after \">>@\""
                doInvoke=True
            else:
                outfile=command[1].strip()
            outfile=tools.redirectFiles(globals()[command[0].strip()],outfile)
            if outfile=="BADINPUT":
                return "*** cancel outputting the file"
            if doInvoke:
                tools.invokeFiles(outfile)

        else:
            try:
                exec("print "+line) in globals()
            except:
                traceback.print_exc()

    def writehist(self):
        try:
            import readline
            readline.set_history_length(80)
            readline.write_history_file()
        except ImportError:
            try:
                import pyreadline as readline
                readline.set_history_length(80)
                readline.write_history_file()
            except ImportError:
                pass

    def get_bosh_global_var_with_filter(self):
        f = ['re', 'readline', 'cmd', 'getpass', 'rpcshell', 'tools', 'csvloader',  'main', 'sys',  'texttable', 'baseCmd', 'adminCmd', 'traceback', 'urlparse',  'os']
        return [v for v in globals().keys() if not v.startswith('_') and not v in f]

    def do_SETPROMPT(self, line):
        self.prompt = line
    def do_setprompt(self, line):
        self.prompt = line

    def do_BOURL(self,line):
        self.do_bourl(line)
    def do_bourl(self,line):
        if self.bosrv_url != line:
            url_object = urlparse(line)
            self.bosrv_url=line
            self.connargs["origin"] = line
            self.connargs["host"] = url_object.hostname if url_object.hostname !=None else self.connargs["host"]
            self.connargs["port"] = url_object.port if url_object.port !=None else self.connargs["port"]

    def do_LISTVAR(self, line):
        self.do_listvar(line)

    def do_listvar(self, line):
        print "all variables: "
        print self.get_bosh_global_var_with_filter()
    def do_SETHOST(self, line):
	self.do_sethost(line)
    def do_sethost(self, line):
        if line != "":
            self.connargs["host"] = line

    def do_SETPORT(self, line):
	self.do_setport(line)
    def do_setport(self, line):
        if line != "":
            self.connargs["port"] = line

    def default(self, line):
	try:
        	exec(line) in globals()
        except:
        	traceback.print_exc()
	

    ##### db test ######################################
    def do_SHOWDB(self, line):
	self.do_showdb(line)
    def do_showdb(self, line):
	dbop.showdb()

    def do_SETDB(self, line):
	self.do_setdb(line)
    def do_setdb(self, line):
	dbop.setdb()

    def do_COPY(self, line):
	self.do_copy(line)
    def do_copy(self, line):
	dbop.copy(line , self.connargs["host"], self.connargs["port"])

    def do_LOAD(self, line):
	self.do_load(line)
    def do_load(self, line):
	print line[:4]
	if line[:4] == "data" or line[:4] == "DATA":
		print "load data : "
		rpcshell.shell(self.connargs, "" , "load " + line)
	else:
		print "load db : "
		dbop.load(line , self.connargs["host"], self.connargs["port"])

    def do_APPEND(self, line):
	self.do_append(line)
    def do_append(self, line):
	dbop.append(line , self.connargs["host"], self.connargs["port"])

    ############## help ################
    def help_column(self):
        print "\tex. b=column 1 in a \n\tb=column 2,4 in a"
    def help_row(self):
        print "\tex. b=row 1 in a \n\tb=row 2,4 in a"
    def help_sql(self):
        print "\trun star-sql shell"
    def help_admin(self):
        print "\trun admin shell"
    def help_find(self):
        tools.print_help_string('assoc_find')
    def help_create(self):
        tools.print_help_string('assoc_associate')
    def help_query(self):
        tools.print_help_string('assoc_query')
    def help_show(self):
        print "\tlist resource in the shell\n\tex. show [tables | association ]"
    def help_desc(self):
        print "\tshow meta-information of a resource\n\tex. desc [association] <name>"
""" #help from sql
    def help_select(self):
        tools.print_help_string('sql_select')
    def help_create(self):
        tools.print_help_string('sql_create')
    def help_insert(self):
        tools.print_help_string('sql_insert')
    def help_update(self):
        tools.print_help_string('sql_update')
    def help_desc(self):
        #print "\tlist table's attribute\n\tdesc <table name>"
        tools.print_help_string('sql_desc')
    def help_show(self):
        #print "\tlist all BigObject tables in workspace\n\tshow tables"
        tools.print_help_string('sql_show')
    def help_syntaxout(self):
        tools.print_help_string('sql_syntaxout')
"""

def main():
    host = "localhost"
    port = "9090"
    token = ""
    bo_url = os.environ.get('BIGOBJECT_URL')
    if bo_url != None:
        url_object = urlparse(bo_url)
        host = url_object.hostname
        port = url_object.port
    else:
        bo_url="bo://localhost:9090"    

    newcmd = baseCmd()
    newcmd.bosrv_url = bo_url
    newcmd.connargs={}
    newcmd.connargs["host"] = host
    newcmd.connargs["port"] = port
    newcmd.connargs["timeout"] = 9999
    newcmd.connargs["workspace"]= ""
    newcmd.connargs["opts"]=""
    newcmd.connargs["origin"]=bo_url
    newcmd.prompt = "bosh>"
    newcmd.intro = "\nWelcome to the BigObject shell\n\nenter 'help' for listing commands\nenter 'quit'/'exit' to exit bosh"
    newcmd.init_complete()
    try:
        newcmd.cmdloop()
    except KeyboardInterrupt:
        print "exiting by KeyboardInterrupt"
        newcmd.writehist()
    print "Thanks for using bosh..."

if __name__ == '__main__':
    main()
