import boshC3
#import boshExcel
import docSql
import os
import json
import sys
def psql_run(d_host, d_port, d_user, d_pass, d_db):
    import getpass
    import os
    host = raw_input(">>> host [" + d_host + "] : " )
    if host != "":
        d_host = host
    port = raw_input(">>> port [" + str(d_port) + "] : " )
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

    psql_str = "PGPASSWORD=" + d_pass + " psql -h " + d_host + " -p " + str(d_port) + " -U " + d_user + " " + d_db
    os.system(psql_str)

#def split_var(statement)
#       firstword = statement.split()[0]
#       if firstword.find("=") != -1:
#               var_name = firstword.split('=')[0]
#               command_str = firstword.split('=')[1:]


#def parse_associate_string_for_display(line):
#       command = line.split(':=')
#       if len(command) >= 2:
#               assoc_name=command[0]
#               assoc_part=command[1].split()
#
#               input_attr = ""
#               output_attr = ""
#               source_data = ""
#               related_attr = ""
#               where_str = ""
#               flag = 0
#
#               for word_index in range(len(assoc_part)):
#
#                       if assoc_part[word_index] != 'associate' and assoc_part[word_index] != 'with' and assoc_part[word_index] != 'from' and assoc_part[word_index] != 'by' and assoc_part[word_index] != 'where':
#                               if assoc_part[word_index - 1] == 'associate':
#                                       input_attr = assoc_part[word_index]
#                               elif assoc_part[word_index - 1] == 'with':
#                                       output_attr = assoc_part[word_index]
#                               elif assoc_part[word_index - 1] == 'from':
#                                       source_data = assoc_part[word_index]
#                               elif assoc_part[word_index - 1] == 'by':
#                                       flag = 0
#                                       related_attr = assoc_part[word_index]
#                               elif assoc_part[word_index - 1] == 'where':
#                                       flag = 1
#                                       where_str += assoc_part[word_index] + " "
#                               else:
#                                       if flag == 0:
#                                               related_attr += assoc_part[word_index] + " "
#                                       else:
#                                               where_str += assoc_part[word_index] + " "
#               print "\nCounting the occurrences of \"" + related_attr + "\" among all \"" + input_attr + "\" X \"" + output_attr + "\" combinations from source \"" + source_data + "\""
#               if where_str != "":
#                       print " with the filter " + where_str
#       else:
#               print "Syntax error: use ':=' to assign the associate name"

def print_help_string(func_name):
    switch_dict = {
    'sql_select': docSql.Select,
    'sql_create': docSql.Create,
    'sql_insert': docSql.Insert,
    'sql_update': docSql.Update,
    'sql_copy': docSql.Copy,
    'sql_load': docSql.Load,
    'sql_show': docSql.Show,
    'sql_desc': docSql.Desc,
    'sql_starschema':docSql.Starschema,
    'sql_syntaxout':docSql.Syntaxout,
    'assoc_associate': docAssocAssociate,
    'assoc_query': docAssocQuery,
    'assoc_analyze': docAssocAnalyze,
    'assoc_find': docFindAnalyze,
    }
    func = switch_dict[func_name]
    result = func()
    return result

def docFindAnalyze():
    print '\n'.join(["find top 10 Product.brand by sum(Data) from sales"
                    ,"find top 10 Product.brand, Customer.gender by sum(Data) from sales"
                    ,"find Product.id by sum(Data) from sales"
                    ,"find Product.brand, Customer.gender, sum(Data) from sales"
                    ,"find Product.brand sum(Data) from sales"
                    ,"find distinct Product.id from sales where Product.brand='Fanta'"
                    ,"find distinct Product.brand, Customer.gender by Customer.gender from sales where Product.brandOwner='Pepsico'"
                    ,"find top 5 Product.brand,Customer.gender, Date by Date from sales"
                    ,"find id from Product where brandOwner='Pepsico'"
                    ,"find name, brand from Product where brandOwner='Pepsico'"
                    ])
def docAssocAnalyze():
    print '\n'.join(["\tanalyze sum(fact_attribute)"
                    ,"\tfrom tablename"
                    ,"\tgroup by attribute1, attribute2, ..."
                    ,"\n\tex."
                    ,"\tanalyze sum(sales)"
                    ,"\tfrom Fact.bt"
                    ,"\twhere date >= '2013-01-01' AND date <= '2013-12-31' AND Product.category = 'electronics'"
                    ,"\tgroup by Customer.gender, date.quarter"
                    ])
def docAssocQuery():
    print '\n'.join(["\t query <query attribute value> from <assoc_name> [by <post_processing1>, <post_processing2>, ...]"
                    ,"\t\t post_processing:"
                    ,"\t\t\tsort_asc : sort the result in ascending order"
                    ,"\t\t\tsort_desc : sort the result in descending order"
                    ,"\t\t\tlimit n: limit the size (n) of query result"
                    ,"\t\t\ttop n: show the top n results"
                    ,"\t\t\tnorm : normalized by the query attribute value's counts in the dataset"
                    ,"\t\t\tthres n: use n as a threshold to filter results"
                    ,"\t\t\tcosine : implementation of cosine similarity"
                    ])

def docAssocAssociate():
    print '\n'.join(["\t "
                    ,"\t\tcreate association <association_name>(<query attribute> to <result attribute>) from <bt name> \n\t\t\tby <related attribute> [, <related attribute>,...] [where <where statement>]"
                    ,"\t\t ex."
                    ,"\t\t create association test(Product.brand to Product.brand) from sales by Customer.id"
                    ])

def docSqlCopy():
    print '\n'.join(["\tcopy table_name_in_database from \"data_source_string\""
                    ,"\twhere condition"
                    ,"\tlink column1=reference_attribute1 and column2=reference_attribute2 ..."
                    ,"\tfact columni"
                    ,"\tkey (column1, ...)"
                    ,"\n\tex."
                    ,"\tcopy sales from \"type=postgresql host=127.0.0.1 port=5432 user=test password=pass db=testdb\""
                    ,"\twhere date > '2013-01-01'"
                    ,"\tlink cid=Customer.id and pid=Product.id"
                    ,"\tfact sales"
                    ,"\n\tcopy Product from \"type=mysql host=127.0.0.1 port=3306 user=root password=test db=testdb\" key (id)"
                    ])
def docSqlLoad():
    print "\tload table_url from \"data_source_string\" \n\tby \"select_statment\"\n\tex.\n\tload sales.bt from \"type=postgresql host=127.0.0.1 port=5432 user=test password=pass db=testdb\" by 'SELECT \"cid\", \"pid\", \"date\", \"sales\" from \"sales\"'"

def docSqlUpdate():
    print "\tUPDATE tablename SET column1=value1, column2=value2, ...\n\tWHERE filter condition\n\n\tex.\n\tUPDATE customber.bt SET state=Ohio WHERE name='Kelly George'"
def docSqlSelect():
    print '\n'.join(["\tselect sum(fact_attribute)"
                    ,"\tfrom tablename"
                    ,"\tgroup by attribute1, attribute2, ..."
                    ,"\n\tex."
                    ,"\tselect sum(sales)"
                    ,"\tfrom Fact.bt"
                    ,"\twhere date >= '2013-01-01' AND date <= '2013-12-31' AND Product.category = 'electronics'"
                    ,"\tgroup by Customer.gender, date.quarter"
                    ,"\n"
                    ,"\tselect distinct attr from tree"
               ])

def docSqlCreate():
    print '\n'.join(["\tcreate table tablename (column1 data-type, [column2 data-type], ...)"
                    ,"\n\tex."
                    ,"\tcreate table log.bt (session_id INT64, url STRING)"
                    ,"\tcreate table Fact.bt (Customer.id STRING, Product.id STRING,"
                    ,"\tdate DATETIME64, fact sales FLOAT,"
                    ,"\tdim (Customer Customer.bt, Product Product.bt))"
                    ,"\n"
                    ,"\tcreate tree bo_name from source_bt group by attr1,attr2,... where cond1,cond2,..."
                    ,"\tcreate fulltree bo_name from source_bt group by attr1,attr2,... where cond1,cond2,..."
               ])
def docSqlInsert():
    print '\n'.join(["\tinsert into tablename values (value1, value2, ...)"
                    ,"\n\tex."
                    ,"\ninsert into customber.bt values ('6', 'Lois Bennett', 'Norwegian', 'Maryland', 'Mydo', 'Female')"
                    ,"\tinsert into Fact.bt values ('2731', '3083', '2013-01-03 02:09:42', 16.85),"
                    ,"\t('4241', '2472', '2013-01-03 02:09:45', 21.05)"
               ])




def dump2Csv(result_table,outfile,line_count,status="append"):
    outfile=outfile if outfile!=None else "dump_result.csv"
    if ".csv" not in outfile:
        outfile+=".csv"
    import csv
    writemode="w" if status=="init" else "a"
    local_count=line_count
    with open(outfile,writemode) as csvfile:
        writer=csv.writer(csvfile)
        for row in result_table:
            writer.writerow([unicode(s).encode("utf-8") for s in row])
            local_count+=1
            sys.stdout.write("\r")
            sys.stdout.write("dump "+str(local_count)+" lines")
            sys.stdout.flush()

    return outfile

def redirectFiles(result_table,outfile):
    if ".html" in outfile:
        outfile=boshC3.Default_output(result_table,outfile)
    elif ".xlsx" in outfile:
        template=outfile if os.path.exists(outfile) else None
        boshExcel.Default_output(result_table,template=template,output=outfile)
    elif ".csv" in outfile:
        import csv
        with open(outfile,"w") as csvfile:
            writer=csv.writer(csvfile)
            for row in result_table:
                writer.writerow([unicode(s).encode("utf-8") for s in row])

    else:
        fd=open(outfile,"w")
        jsonstr=json.dumps(result_table)
        fd.write(jsonstr)
        fd.close()
    print "Write into file: "+os.path.abspath(outfile)
    return outfile


def invokeFiles(outfile):
    from subprocess import Popen
    import platform
    try:
        # saverr=os.dup(2)
        # os.close(2)
        if "Darwin" in platform.system():
            Popen(["open",outfile])
        elif os.name=="posix":
            Popen(["xdg-open",outfile])
        elif os.name=="nt":
            Popen(["open",outfile])
        else:
            print "Invoke function is not supported under your os environment."
    finally:
        # os.dup2(saverr,2)
        pass



def postactionParser(command_str):
    parsedict={"command":None,"out_command":None,"pipes_command":None,"ERR_msg":None,"doInvoke":False}
    parsedict["command"]=command_str

    splits=command_str.split(">>")
    if len(splits)>=2:
        if len(splits[1])==0:
            parsedict["ERR_msg"]="*** FILENAME required after \">>\""
            return parsedict
        elif "|" in splits[1]:
            parsedict["ERR_msg"]="*** Operations via PIPES should be put before \">>\""
            return parsedict
        elif "@" in splits[1]:
            outfile=splits[1][splits[1].find("@")+1:].strip()
            if len(outfile)==0:
                parsedict["ERR_msg"]="*** FILENAME required after \">>@\""
                return parsedict
            parsedict["doInvoke"]=True
            parsedict["out_command"]=outfile
        else:
            parsedict["out_command"]=splits[1].strip()

        parsedict["command"]=splits[0].strip()


    splits=parsedict["command"].split("|")
    if len(splits)>=2:
        if len(splits[1])==0:
            parsedict["ERR_msg"]="*** PROGRAM/COMMAND required after \"|\""
            return parsedict
        strBegin=parsedict["command"].find("|")
        parsedict["pipes_command"]=parsedict["command"][strBegin+1:]
        parsedict["command"]=splits[0]



    return parsedict


def runPipes(result_table,pipes_command):
    from subprocess import Popen, PIPE
    jsonstr=json.dumps(result_table)
    command=pipes_command.split()

    process=Popen(command,stdin=PIPE)  #use STDIN to send data, could use linux build-in commands easily
    process.stdin.write(jsonstr)

    #command.append(jsonstr)    # append data (jsonstr) as the last arguments
    #process=Popen(command)

    process.communicate()



