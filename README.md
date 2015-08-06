# BOSH - a BigObject shell

**bosh** is a python command-line interface for a BigObject server

##System requirements
Python 2.7

## Getting BigObject

BigObject server provides storage and analytic computation for your data.
These feature endpoints are made available through BigObject query language,

Refer to the full documentation [here](https://docs.bigobject.io/)

We recommend you build your BigObject server through
[Docker Hub](https://registry.hub.docker.com/u/macrodata/bigobject/).  Other options available through custom
request via info@macrodatalab.com

## Getting BOSH

The recommended way for getting BOSH is through the python package management tool "pip" :

```bash
$ pip install bosh
```

**pip** is a popular python package management tool.  Get pip
[here](https://pip.pypa.io/en/latest/installing.html)

Verify bosh is install be excuting **bosh** in your terminal
 
Use the environment variable **BIGOBJECT_URL**  to set the BigObject server url

ex. BIGOBJECT_URL=bo://127.0.0.1:9090 bosh

The default BIGOBJECT_URL setting: localhost:9090 

```bash
$ BIGOBJECT_URL=<url_to_bigobject_service> bosh
Welcome to the BigObject shell

enter 'help' for listing commands
enter 'quit'/'exit' to exit bosh
bosh>
```

# bosh commands
## csvloader
Load a table data from a CSV file (ex. data.csv). The table (ex. datatable) should be pre-created.
```bash
bosh>admin
bosh:admin>csvloader data.csv datatable
```

## luaupload
Upload a lua script to the BigObject server
```bash
bosh>admin
bosh:admin>luaupload test.lua
```

## change server
```bash
bosh>sethost 192.168.1.111
bosh>setport 9090
```

