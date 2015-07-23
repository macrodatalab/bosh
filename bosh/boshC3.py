def htmlTag(f):
    def wrapper(*args,**kwargs):
        return "<html>\n"+str(f(*args,**kwargs))+"\n</html>\n"
    return wrapper

def scriptTag(f):
    def wrapper(*args,**kwargs):
        return "<script>\n"+str(f(*args,**kwargs))+"\n</script>\n"
    return wrapper

def bodyTag(f):
    def wrapper(*args,**kwargs):
        return "<body>\n"+str(f(*args,**kwargs))+"\n</body>\n"
    return wrapper

def divTagTail(f):
    def wrapper(*args,**kwargs):
        return str(f(*args,**kwargs))+"\n</div>\n"
    return wrapper

def styleTag(f):
    def wrapper(*args,**kwargs):
        return "<style>\n"+str(f(*args,**kwargs))+"\n</style>\n"
    return wrapper

def docReady(f):
    def wrapper(*args,**kwargs):
        strFuncBegin="""
          $(document).ready(function ()
          {\n
        """
        strFuncEnd="""
           \n
           });
        """
        return strFuncBegin+str(f(*args,**kwargs))+strFuncEnd
    return wrapper




class BaseHtml(object):
    def _insertOneline(self,strOneline):
        return strOneline+"\n"

    @divTagTail
    def _createDiv(self,strAttr,divElements=str()):
        return "<div "+strAttr+">\n"+divElements

    @scriptTag
    def _insertScript(self,strScript):
        return strScript

    @bodyTag
    def _insertLayout(self,strDiv):
        return strDiv

    def writeHTML(self,outFile="default.html"):
        htmlfile=open(outFile,"w")
        htmlfile.write(self._strHTML)
        htmlfile.close()

    @property
    def strHTML(self):
        return self._strHTML

    def checkQuote(self,jsondata):
        jsondata=str(jsondata).replace("'","")
        return jsondata




class C3(BaseHtml,object):
    def __init__(self,jsonData,chartType="bar"):
        self._strHTML=self._genHTML(jsonData,chartType)


    @docReady
    def _loadJSDocReady(self,data,**kwargs):

        strDocReady='var data={};\n'.format(str(data))
        strDocReady+='var bo=BigObject_D3Chart;\n\n\n'
        for bindID,chartType in kwargs.items():
            strDocReady += 'bo.draw_LocalData(data,"{}","#{}",600);\n'.format(chartType,bindID)
            bindID


        return strDocReady+"\n"


    def _insertJSCSSlib(self):
        strJSCSS=str()
        strJSCSS+=self._insertOneline("""<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>""")
        strJSCSS+=self._insertOneline("""<script src="http://d3js.org/d3.v3.min.js"></script> """)
        strJSCSS+=self._insertOneline("""<link href="https://cdn.rawgit.com/masayuki0812/c3/master/c3.min.css" rel="stylesheet" type="text/css">""")
        strJSCSS+=self._insertOneline("""<script src="http://cdn.rawgit.com/masayuki0812/c3/master/c3.js"></script>""")
        strJSCSS+=self._insertOneline("""<script src="BigObject.js"></script>""")
        return strJSCSS






    @htmlTag
    def _genHTML(self,jsonData,chartType):
        chartDIV=self._createDiv(""" id="chart1" """)
        strDIV=self._createDiv(""" class="containerLeft" """,divElements=chartDIV)
        listChart={"chart1":chartType}
        strJS=self._loadJSDocReady(jsonData,**listChart)

        html_string=str()
        html_string+=self._insertJSCSSlib()
        html_string+=self._insertScript(strJS)
        html_string+=self._insertLayout(strDIV)
        return html_string

class D3_Chord(BaseHtml,object):
    def __init__(self,matrix,datagroups,chartType="bar"):
        self._strHTML=self._genHTML(matrix,datagroups,chartType)


    @docReady
    def _loadJSDocReady(self,matrix,datagroups):
        strDocReady='var matrix={};\n\n'.format(matrix)
        strDocReady+='var datagroups={};\n\n'.format(datagroups)
        strDocReady+='var bochart=BigObject_D3Chart;\n\n\n'
        strDocReady+='bochart.Association_LocalData(datagroups,matrix);'

        return strDocReady+"\n"

    @styleTag
    def _insertCSS(self):
        strMYCSS=str()
        strMYCSS="""
        #circle circle {
        fill: none;
        pointer-events: all;
        }

        .group path {
        fill-opacity: .5;
        }

        path.chord {
        stroke: #777;
        stroke-width: 0.1px;
        }

        #circle:hover path.fade {
        display: none;
        }
                  """
        return strMYCSS+"\n"


    def _insertJSCSSlib(self):
        strJSCSS=str()
        strJSCSS+=self._insertOneline("""<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>""")
        strJSCSS+=self._insertOneline("""<script src="http://d3js.org/d3.v3.min.js"></script> """)
        strJSCSS+=self._insertOneline("""<link href="https://cdn.rawgit.com/masayuki0812/c3/master/c3.min.css" rel="stylesheet" type="text/css">""")
        strJSCSS+=self._insertOneline("""<script src="http://cdn.rawgit.com/masayuki0812/c3/master/c3.js"></script>""")
        strJSCSS+=self._insertOneline("""<script src="BigObject.js"></script>""")
        return strJSCSS






    @htmlTag
    def _genHTML(self,matrix,datagroups,chartType):
        strJS=self._loadJSDocReady(matrix,datagroups)

        html_string=str()
        html_string+=self._insertCSS()
        html_string+=self._insertJSCSSlib()
        html_string+=self._insertScript(strJS)
        return html_string




def buildChordData(data):
    if len(data[0])!=3 :
        return None
    datacol1=[row[0].strip() for row in data]
    datacol2=[row[1].strip() for row in data]
    datagroups=list(set(datacol1+datacol2))

    iddict={j:i for i,j in enumerate(datagroups)}
    matrix=[[0 for i in range(0,len(datagroups))] for i in range(0,len(datagroups))]

    for row in data:
        rowid=iddict[row[0].strip()]
        colid=iddict[row[1].strip()]
        matrix[rowid][colid]=row[2]

    return [matrix,datagroups]

def Default_output(result_table,filestr="default.html"):
        #import webbrowser
    chartType="bar"
    url=filestr
    if "-t" in filestr:
        listChartTypes=["pie","bar","line","spline","assoc"]
        tmpCmd=filestr.split("-t")
        chartType=tmpCmd[1].strip()
        if chartType not in listChartTypes:
            print "only supports following chartTypes: " +str(listChartTypes)
            print "Your expected chartType: "+chartType
            return "BADINPUT"

        if len(tmpCmd[0])==0:
            print "*** FILENAME required after \">>@\""
            return "BADINPUT"

        url=tmpCmd[0].strip()


    import json
    if chartType=="assoc":
        packdata=buildChordData(result_table)
        if packdata==None:
            print "Set format is not correct: "
            print result_table[0]
            return "BADINPUT"

        matrix=packdata[0]
        datagroups=packdata[1]
        chart=D3_Chord(json.dumps(matrix),json.dumps(datagroups))
    else:
        chart=C3(json.dumps(result_table),chartType)
    chart.writeHTML(url)
    return url
