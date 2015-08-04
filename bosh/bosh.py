import sys
import cmd
import os
import rpcshell
import re
import csvloader
from urlparse import urlparse
import tools
import getpass
import traceback

class adminCmd(cmd.Cmd):
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
                print csvloader.csvload(self.connargs, input_line[0] , input_line[1])
            else:
                print "csvloader <csv_file> <bt_name>"
    def do_info(self, line):
        print "host : " + self.connargs["host"]
        print "port : " + str(self.connargs["port"])
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
    assocword = [ 'create' , 'find', 'select' , 'build' , 'use' , 'apply' , 'get' ,'insert' , 'update' , 'alter', 'association', 'from' , 'by' , 'where' , 'query' , 'tables' , 'from', 'by', 'group by' , 'where' , 'tree' , 'table' , 'workspace' ]
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

    def completedefault(self, text, line, begidx, endidx):
        if not text:
            completions = self.assocword[:]
        else:
            completions = [ f
            for f in self.assocword
            if f.startswith(text)
            ]
        return completions

    ############# BigObject ##############
    def do_CREATE(self, line):
        self.do_create(line)
    def do_create(self, line):
        print rpcshell.shell(self.connargs, "" , "create " + line)
    def do_BUILD(self, line):
        self.do_build(line)
    def do_build(self, line):
        rpcshell.shell(self.connargs, "" , "build " + line)
    def do_USE(self,line):
        self.do_use(line)
    def do_use(self,line):
        cmdSplits=line.split()
        if cmdSplits[0] != "workspace":
            print "usage: use workspace <workspace_name>"
            return
        wsStr=cmdSplits[1] if len(cmdSplits) > 1 else ""
        if wsStr=="default" or wsStr=="":
            self.connargs["workspace"]=""
       	    rpcshell.shell(self.connargs, "" , "use workspace default")
        else:
            self.connargs["workspace"]=wsStr
            sqlStr="create workspace "+wsStr
	    rpcshell.shell(self.connargs, "" , "use " + line)
        print "switch to workspace:" +str(wsStr)
	
    def do_SHOW(self,line):
        self.do_show(line)
    def do_show(self, line):
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
    def do_DROP(self,line):
        self.do_drop(line)
    def do_drop(self, line):
        rpcshell.shell(self.connargs, "" , "drop " + line)
    def do_TRIM(self,line):
        self.do_trim(line)
    def do_trim(self, line):
        rpcshell.shell(self.connargs, "" , "trim " + line)
    def do_SELECT(self, line):
        self.do_select(line)
    def do_select(self, line):
        rpcshell.shell(self.connargs, "" , "select " + line , True)
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

    ##################### bosh ###########################
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
        print "workspace : " + str(self.connargs["workspace"])

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

    def do_sethost(self, line):
        if line != "":
            self.connargs["host"] = line
    def do_setport(self, line):
        if line != "":
            self.connargs["port"] = line
    def default(self, line):
	try:
        	exec(line) in globals()
        except:
        	traceback.print_exc()

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

    try:
        newcmd.cmdloop()
    except KeyboardInterrupt:
        print "exiting by KeyboardInterrupt"
        newcmd.writehist()
    print "Thanks for using bosh..."

if __name__ == '__main__':
    main()
