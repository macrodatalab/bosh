class color:
    PURPLE = ''
    YELLOW = ''
    RED = ''
    BOLD = ''
    UNDERLINE = ''
    END = ''


def enableColor():
    tmpColor=color()
    color.PURPLE ='\033[95m'
    color.YELLOW = '\033[93m'
    color.RED = '\033[91m'
    color.BOLD = '\033[1m'
    color.UNDERLINE = '\033[4m'
    color.END = '\033[0m'



def disableColor():
    tmpColor=color()
    color.PURPLE=''
    color.YELLOW=''
    color.RED=''
    color.BOLD=''
    color.UNDERLINE=''
    color.END=''


def LayoutSpace(f):
    def wrapper(*args,**kwargs):
        print
        f(*args,**kwargs)
        print
    return wrapper


def cmd(cmdstr):
    return color.BOLD+color.YELLOW+cmdstr+color.END

def emphasis(hltstr):
    return color.BOLD+hltstr+color.END



def arguments(argstr):
    return color.BOLD+color.RED+argstr+color.END

def http(httpstr):
    return color.UNDERLINE+httpstr+color.END


@LayoutSpace
def Show():
    print '\n'.join(["\tshow: List all BigObject tables stored in current workspace."
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\t{0}".format(cmd("show tables"))
                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\tList all BigOject tables' tablename, seperated by a comma and followed by a newline."
                    ,emphasis("\n\tSEE ALSO:")
                    ,"\t\tUse \"{0}\" to look into details of the specific table.".format(cmd("desc"))
                    ,"\t\tType \"{0}\" for more information.".format(cmd("help desc"))
                   ])


@LayoutSpace
def Desc():
    print '\n'.join(["\tdesc: List details of the table assigned with {0} argument. ".format(arguments("TABLENAME"))
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\t{0} {1}".format(cmd("desc"),arguments("TABLENAME"))
                    ,"\n\t\tex."
                    ,"\t\t{0} {1}".format(cmd("desc"),arguments("Products"))
                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\t{0} lists following details of a table:".format(cmd("desc"))
                    ,emphasis("\t\t    size: ")+"the number of records in the table."
                    ,emphasis("\t\t    schema: ")+"the descriptions of table attributes."
                    ,emphasis("\t\t    dimensions: ")+"the lists of related dimensions in the table."
                    ,emphasis("\t\t    name: ")+"the table name."
                    ,"\t\tThere are two kinds of tables in BigOject: dimension table and fact table."
                    ,"\t\tIf {0} ".format(emphasis("dimensions"))+"have no instance in it, then the described table is a dimension table."
                    ,emphasis("\n\tSEE ALSO:")
                    ,"\t\tThe definition of table types in BigObject could be found in:"
                    ,"\t\t{0}".format(http("http://docs.macrodatalab.com/tutorial/table-object.html"))
                    ,"\t\tA more powerful version of \"{0}\" is \"{1}\".".format(cmd("desc"),cmd("starschema"))
                    ,"\t\tType \"{0}\" for more information.".format(cmd("help starschema"))
                   ])


@LayoutSpace
def Starschema():
    print '\n'.join(["\tstarschema: Show the table's meta information including related tables."
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\t{0} {1}".format(cmd("starschema"),arguments("TABLENAME"))
                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\t{0} lists meta information of a table:".format(cmd("starschema"))
                    ,emphasis("\t\t    measures: ")+"the attributes in table to be analyized, also named as fact attributes."
                    ,emphasis("\t\t    attrs: ")+"the non-measure attributes."
                    ,emphasis("\t\t    name: ")+"the table name."
                    ,emphasis("\t\t    dimensions: ")+"the meta information of each dimension, displayed as nested structures."
                    ,"\t\tThere are measure attributes and non-measure attributes in a fact table.\"{0}\" will list both of them seperately."
                    .format(cmd("starschema"))
                    ,"\t\tMoreover,if the non-measure attribute is a dimension, the details of the table related to this dimension "
                    ,"\t\twill also be listed in the output."
                    ,emphasis("\n\tSEE ALSO:")
                    ,"\t\tThe definition of table types in BigObject could be found in:"
                    ,"\t\t{0}".format(http("http://docs.macrodatalab.com/tutorial/table-object.html"))
                   ])


@LayoutSpace
def Create():
    print '\n'.join(["\tcreate: Create a BigObject object."
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\t{0} {1} {2}".format(cmd("create table"),
                                              arguments("TABLENAME"),
                                              cmd("(")+arguments("ATTR1 DATATYPE [,ATTR2 DATATYPE ...]")+cmd(")")
                                             )
                    ,"\t\t{0} {1} {2} {3} {4} {5} {6} {7}".format(cmd("create tree"),
                                                                  arguments("BO_NAME"),
                                                                  cmd("from"),
                                                                  arguments("SOURCE_BT"),
                                                                  cmd("group by"),
                                                                  arguments("ATTR1 [,ATTR2 ...]"),
                                                                  cmd("where"),
                                                                  arguments("CONDITION1 [,CONDITION2 ...]")
                                                                 )
                    ,"\t\t{0} {1} {2} {3} {4} {5} {6} {7}".format(cmd("create fulltree"),
                                                                  arguments("BO_NAME"),
                                                                  cmd("from"),
                                                                  arguments("SOURCE_BT"),
                                                                  cmd("group by"),
                                                                  arguments("ATTR1 [,ATTR2 ...]"),
                                                                  cmd("where"),
                                                                  arguments("CONDITION1 [,CONDITION2 ...]")
                                                                 )
                    ,"\n\t\tex."
                    ,"\t\t{0} {1} {2}".format(cmd("create table"),
                                              arguments("log"),
                                              cmd("(")+arguments("session_id INT64,url STRING")+cmd(")")
                                             )
                    ,"\t\tex. create a dim table"
                    ,"\t\t{0} {1} {2}".format(cmd("create table"),arguments("Product"),cmd("("))
                    ,"\t\t                     {0}".format(arguments("id STRING,"))
                    ,"\t\t                     {0}".format(arguments("name STRING,"))
                    ,"\t\t                     {0}".format(arguments("brand STRING,"))
                    ,"\t\t                     {0}".format(arguments("KEY(id)"))
                    ,"\t\t                     {0}".format(cmd(")"))
                    ,"\t\tex. create a fact table"
                    ,"\t\t{0} {1} {2}".format(cmd("create table"),arguments("Fact"),cmd("("))
                    ,"\t\t                     {0}".format(arguments("Customer.id STRING,"))
                    ,"\t\t                     {0}".format(arguments("Product.id STRING,"))
                    ,"\t\t                     {0}".format(arguments("date DATETIME64,"))
                    ,"\t\t                     {0} {1}".format(cmd("fact"),arguments("sales FLOAT,"))
                    ,"\t\t                     {0}{1}{2}".format(cmd("dim ("),arguments("Customer Customer.bt, Product Product.bt"),cmd(")"))
                    ,"\t\t                     {0}".format(cmd(")"))
                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\t{0} can create all kinds of BigObject objects,including TABLE,TREE,FULLTREE.".format(cmd("create"))
                    ,"\t\tWe use \"{0}\" to create BigObject table.".format(cmd("create table"))
                    ,"\t\tBased on the table, we could construct TREE or FULLTREE by \"{0}\" and \"{1}\" respectively."
                                                                    .format(cmd("create tree"),cmd("create fulltree"))
                    ,emphasis("\n\tSEE ALSO:")
                    ,"\t\tBigObject supports several operations on tables."
                    ,"\t\tUse \"{0}\", \"{1}\" to check table schema.".format(cmd("desc"),cmd("starschema"))
                    ,"\t\tTry \"{0}\", \"{1}\" ,and \"{2}\" for table operations.".format(cmd("drop"),cmd("insert"),cmd("update"))
                    ,"\t\tUse \"{0}\" to fetch data. Type \"{1} {2}\" for details.".format(cmd("select"),cmd("help"),arguments("ABOVE_CMD"))

               ])


@LayoutSpace
def Insert():
    print '\n'.join(["\tinsert: Insert data into a table."
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\t{0} {1} {2} {3}".format(
                                                  cmd("insert into"),
                                                  arguments("TABLENAME"),
                                                  cmd("values"),
                                                  cmd("(")+arguments("VALUE1 [,VALUE2 ...]")+cmd(")")
                                                 )
                    ,"\n\t\tex."
                    ,"\t\t{0} {1} {2} {3}".format(
                                                  cmd("insert into"),
                                                  arguments("customer.bt"),
                                                  cmd("values"),
                                                  cmd("(")+arguments("""'6', 'Lois Bennett', 'Norwegian', 'Maryland', 'Mydo', 'Female' """)+cmd(")")
                                                 )
                    ,"\t\t{0} {1} {2} {3}".format(
                                                  cmd("insert into"),
                                                  arguments("Fact.bt"),
                                                  cmd("values"),
                                                  cmd("(")+arguments("""'2731', '3083', '2013-01-03 02:09:42', 16.85 """)+cmd("),")
                                                 )
                    ,"\t\t\t\t\t   {0}".format(cmd("(")+arguments("""'4241', '2472', '2013-01-03 02:09:45', 21.05 """)+cmd(")"))
                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\tInsert data into BigObject table. Follow the examples above, multiple rows of data could be inserted by one command."
                    ,emphasis("\n\tSEE ALSO:")
                    ,"\t\t\"{0}\" and \"{1}\" are also used for table operations.".format(cmd("drop"),cmd("update"))

                   ])


@LayoutSpace
def Update():
    print '\n'.join(["\tupdate: Update existed data in the table."
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\t{0} {1} {2} {3} {4} {5}".format(
                                                  cmd("update"),
                                                  arguments("TABLENAME"),
                                                  cmd("set"),
                                                  arguments("ATTR1=VALUE1 [,ATTR2=VALUE2 ...]"),
                                                  cmd("where"),
                                                  arguments("FILTER CONDITIONS")
                                                 )
                    ,"\n\t\tex."
                    ,"\t\t{0} {1} {2} {3} {4} {5}".format(
                                                  cmd("update"),
                                                  arguments("customer.bt"),
                                                  cmd("set"),
                                                  arguments("state=Ohio"),
                                                  cmd("where"),
                                                  arguments("""name='Kelly George'""")
                                                 )
                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\tUpdate existed data in BigObject table"
                    ,emphasis("\n\tSEE ALSO:")
                    ,"\t\t\"{0}\" and \"{1}\" are also used for table operations.".format(cmd("drop"),cmd("insert"))

                   ])


@LayoutSpace
def Select():
    print '\n'.join(["\tselect: Select data in a table."
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\t{0} {1} {2}".format(
                                                  cmd("select sum(")+arguments("FACT_ATTR")+cmd(")"),
                                                  cmd("from"),
                                                  arguments("TABLENAME"),
                                                 )
                    ,"\t\t\t\t      {0} {1}".format(cmd("where"),arguments("CONDITION1 [AND CONDITION2 ...]"))
                    ,"\t\t\t\t      {0} {1}".format(cmd("group by"),arguments("ATTR1 [,ATTR2 ...]"))
                    ,"\n\t\tex."
                    ,"\t\t{0} {1} {2}".format(
                                                  cmd("select sum(")+arguments("sales")+cmd(")"),
                                                  cmd("from"),
                                                  arguments("Fact.bt"),
                                                 )
                    ,"\t\t\t\t  {0} {1}".format(cmd("where"),arguments("date >= '2013-01-01' AND date <= '2013-12-31' AND Product.category = 'electronics'"))
                    ,"\t\t\t\t  {0} {1}".format(cmd("group by"),arguments("Customer.gender, date.quarter"))
                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\t{0} provides several funtions to derive data in a table.".format(cmd("select"))
                    ,"\t\tSet conditions by using \"{0}\" and group your results by assign attributes with \"{1}\".".format(
                                                  cmd("where"),
                                                  cmd("group by")
                                                                                                                           )
                    ,"\t\tNote that the attribute in \"{0}\" must be a {1}.".format(cmd("select sum()"),emphasis("fact attribute"))
                    ,emphasis("\n\tSEE ALSO:")
                    ,"\t\tThe definition of {0} in BigObject could be found in:".format(emphasis("fact attribute"))
                    ,"\t\t{0}".format(http("http://docs.macrodatalab.com/tutorial/table-object.html"))


                   ])


@LayoutSpace
def Load():
    print '\n'.join(["\tload: load data from external databases"
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\t{0} {1} {2} {3} {4} {5}".format(
                                                  cmd("load"),
                                                  arguments("TABLENAME"),
                                                  cmd("from"),
                                                  arguments("DATASOURCE_STR"),
                                                  cmd("by"),
                                                  arguments("SELECT_STATEMENT")
                                                 )
                    ,"\n\t\tex."
                    ,"\t\t{0} {1} {2} {3}".format(
                                             cmd("load"),
                                             arguments("sales.bt"),
                                             cmd("from"),
                                             arguments("""\"type=postgresql host=127.0.0.1 port=5432 user=test password=pass db=testdb\"""")
                                                )
                    ,"\t\t\t      {0} {1}".format( cmd("by"),
                                    cmd("'")+arguments("""SELECT "cid", "pid", "date", "sales" from "sales\"""")+cmd("'")
                                  )

                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\t{0} loads {1} from external databases, from table to table.".format(cmd("load"),emphasis("selected data"))
                    ,"\t\tCurrently,BigObject supports postgresql and mysql databases."
                    ,"\t\t{0} must contain complete information of connection like the above example.".format(arguments("DATASOURCE_STR"))
                    ,"\t\tDecide attributes you would like to load from an external database with {0} after keyword \"{1}\".".format(
                                                                                                              arguments("SELECT_STATEMENT"),
                                                                                                              cmd("by")
                                                                                                                       )
                    ,emphasis("\n\tSEE ALSO:")
                    ,"\t\t\"{0}\" directly copy a {1} from an external database.Type \"{2}\" for the details.".format(
                                                                                                        cmd("copy"),
                                                                                                        emphasis(" table"),
                                                                                                        cmd("help copy")
                                                                                                        )

                   ])


@LayoutSpace
def Copy():
    print '\n'.join(["\tcopy: Copy tables from external databases."
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\t{0} {1} {2} {3}".format(
                                                  cmd("copy"),
                                                  arguments("TABLENAME"),
                                                  cmd("from"),
                                                  arguments("DATASOURCE_STR"),
                                                 )
                    ,"\t\t\t       {0} {1}".format(cmd("where"),arguments("CONDITIONS"))
                    ,"\t\t\t       {0} {1}".format(cmd("link"),arguments("ATTR1=REF_ATTR1 [and ATTR2=REF_ATTR2 ...]"))
                    ,"\t\t\t       {0} {1}".format(cmd("fact"),arguments("FACT_ATTR"))
                    ,"\t\t\t       {0} {1}".format(cmd("key"),cmd("(")+arguments("KEY_ATTR1 [,KEY_ATTR2 ...]")+cmd(")"))

                    ,"\n\t\tex."
                    ,"\t\t{0} {1} {2} {3}".format(
                                              cmd("copy"),
                                              arguments("sales"),
                                              cmd("from"),
                                              arguments("""\"type=postgresql host=127.0.0.1 port=5432 user=test password=pass db=testdb\""""),
                                                 )
                    ,"\t\t\t   {0} {1}".format(cmd("where"),arguments("date > '2013-01-01'"))
                    ,"\t\t\t   {0} {1}".format(cmd("link"),arguments("cid=Customer.id and pid=Product.id"))
                    ,"\t\t\t   {0} {1}".format(cmd("fact"),arguments("sales"))
                    ,"\t\t{0} {1} {2} {3} {4} {5}".format(
                                              cmd("copy"),
                                              arguments("Product"),
                                              cmd("from"),
                                              arguments("""\"type=mysql host=127.0.0.1 port=3306 user=root password=test db=testdb\""""),
                                              cmd("key"),
                                              cmd("(")+arguments("id")+cmd(")")
                                              )

                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\tUse {0} to directly copy a table from an external database.".format(cmd("copy"))
                    ,"\t\t\"{0}\" supports several functions while loading a table.".format(cmd("copy"))
                    ,"\t\t\"{0}\" is used to set filter conditions on the source table.".format(cmd("where"))
                    ,"\t\tUse keywords \"{0}\" and \"{1}\" to define special types, \"{2}\" and \"{3}\" respectively.".format(
                                              cmd("fact"),
                                              cmd("key"),
                                              emphasis("fact attributes"),
                                              emphasis("key attributes")
                                                                                                                    )
                    ,"\t\tLink attributes in copied table to attributes in pre-defined dimension tables with the keyword \"{0}\"."
                     .format(cmd("link"))
                    ,emphasis("\n\tSEE ALSO:")
                    ,"\t\t\"{0}\" is also used to load external data. Type \"{1}\" for more information.".format(cmd("load"),cmd("help load"))

                   ])



@LayoutSpace
def Syntaxout():
    print '\n'.join(["\tExamples of how to output results into EXCEL or HTML files"
                    ,emphasis("\n\tSYNOPSIS:")
                    ,"\t\tBIGOBJECT_STATMENTS {0} {1}".format(
                                                  cmd(">>"),
                                                  arguments("XLSX_FILENAME"),
                                                 )
                    ,"\t\tBIGOBJECT_STATMENTS {0} {1} {2}".format(
                                                  cmd(">>"),
                                                  cmd("@")+arguments("HTML_FILENAME"),
                                                  arguments("[-t CHARTTYPE]")
                                                 )

                    ,"\n\t\tex."
                    ,"\t\tselect sum(step) from steps group by shoes.brand, users.country {0} {1}"
                     .format(cmd(">>"),arguments("step_country.xlsx"))
                    ,"\t\tselect sum(step) from steps group by shoes.brand, users.country {0} {1}"
                     .format(cmd(">>"),cmd("@")+arguments("step_country.html -t line"))
                    ,emphasis("\n\tDESCRIPTION:")
                    ,"\t\tBesides the stdout, bosh could also output results in Excel or HTML files."
                    ,emphasis("\t\tto Excel:")
                    ,"\t\t\tAdd {0} after BIGOBJECT_STATEMENTS, by which is used to derive data, to assign the output filename."
                     .format(cmd(">>"))
                    ,"\t\t\tThe input string after {0} will be regarded as a Excel file. \"{1}\" will be added if not found in the string."
                     .format(cmd(">>"),emphasis(".xlsx"))
                    ,"\t\t\tIf the assigned file already exists, program will {0} current results as a new sheet in the file."
                     .format(emphasis("append"))
                    ,emphasis("\t\tto HTML:")
                    ,"\t\t\tSimilar syntax to Excel, but need to add an addtional symbol \"{0}\" before output filename.".format(cmd("@"))
                    ,"\t\t\tAlso, \"{0}\" will be added if not found in the filename string.".format(emphasis(".html"))
                    ,"\t\t\tIf the assigned file already exists, program will {0} it.".format(emphasis("overwrite"))
                    ,"\t\t\tThere are three chart types supported here: {0}, {1} and {2}. By default is a barchart, choose one using {3} options"
                     .format(emphasis("bar"),emphasis("line"),emphasis("spline"),cmd("-t"))
                    ,"\t\t\tBosh will attach a new tab if there's already an opened browser, else just launch a new one."
                   ,"\t\t\tAlthough bosh write to local HTML files, some javascript libraries are used thus internet access is required."

                   ])



def dumpALL():
    line="========================================================================================="
    docSqllist=[Show,Desc,Starschema,Create,Insert,Update,Load,Copy,Select,Syntaxout]
    for doc in docSqllist:
        print line
        func=doc
        func()

if __name__=="__main__":
    dumpALL()
