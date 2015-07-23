# BOSH - a BigObject shell

BigObject service provides storage and analytic computation for your data.
These feature endpoints are made available through BigObject query language,
**boql**.  The language are divided into two feature sets, with a single admin
control for list and get metadata opertions.

Refer to the full documentation [here](docs.macrodatalab.com)

## Getting BigObject service

We recommend you provision a BigObject service through
[HEROKU](https://www.heroku.com/).  Other options available through custom
request via info@macrodatalab.com

## Getting BOSH

The recommended way for getting BOSH is through the official cheese factory.

```bash
$ pip install bosh
```

**pip** is a popular python package management tool.  Get pip
[here](https://pip.pypa.io/en/latest/installing.html)

Verify bosh is install be excuting **bosh** in your terminal

```bash
$ BIGOBJECT_URL=<url_to_bigobject_service> bosh
Welcome to the BigObject shell

enter 'help' for listing commands
enter 'quit'/'exit' to exit bosh
$ bosh>
```

## Cross-Link: Build and retrieve association from relations

Cross-Link is an algorithm for building association from relaional data based
on certain attribute value.  Cross-Link allows one to gain insight into their
users behavior, or find new relationships between entities.

Cross-Link works by

- creating a query object from your relational data.
- through built query object, retrieve association index.

Lets say you have a sales data with transactions including customer id and
product id.  The build a query object for understanding how strong two products
relate to each other by customer, you perform the following

```bash
$ bosh> create association pid2pid(pid to pid) from <your sales record> by cid
```

This creates the query object pid2pid on the BigObject service.

You are now ready to make query.  Suppose we are interested in products that
are usually bought together by a customer, we formulate our query in

```bash
$ bosh> query <some product id e.g. 3560> from pid2pid by top 5
result:
[u'1355', 2]
[u'2271', 2]
[u'1733', 2]
[u'84', 2]
[u'2142', 1]
size:5
```

The result shows that product id 3560 is bought together with product id 1355
by a customer 2 times; 1 time with product 2142 with the same customer.

Find out more on Cross-Link analysis language [here](docs.macrodatalab.com).

## BigObject datastructure I/O

Building Cross-Link analysis requires relational data.  To build these source
data, we need a specialized data structure defined under BigObject called
BigTable.

BigTable works like a tradtional RDBMS table, but with pre established links
(join specification) defined at creation time.  This allows us to quickly pull
data from source table by join index.

We need to work with some data, so lets dump these info into a csv file

```bash
$ cat >test.csv <<EOF
"5755","3671","2013-01-01 00:09:49","9.48"
"2165","4058","2013-01-01 00:11:08","6.9"
"9399","392","2013-01-01 00:18:30","6.93"
"1697","24","2013-01-01 00:26:59","11.75"
"8691","3645","2013-01-01 00:32:47","9.15"
"2732","3084","2013-01-01 00:35:42","16.85"
"8695","765","2013-01-01 00:41:04","4.05"
"153","3770","2013-01-01 00:50:19","19.07"
EOF
```

We shall load this csv file into a BigTable.  But first we need a table.

```bash
$ bosh> sql
$ bosh:*sql> create table sample(cid STRING, pid STRING, date DATE32, fact sales DOUBLE)
$ bosh:*sql> exit
$ bosh> admin
$ bosh:admin> csvloader test.csv sample
```

Command above first switches into *starsql* subcommand, then creates an empty
BigTable called *sample* with schema.  Then we switch into admin subcommand to
load our csv file on disk into our BigObject service.

With table built and loaded, we could perform some multi-dimensional analysis
(MDA) with the *starsql* subcommand

```bash
$ bosh> find top 3 cid from sample by sum(sales)
result:
[u'153', 19.07]
[u'2732', 16.85]
[u'1697', 11.75]
size:3
$ bosh> find top 1 pid from sample by date where cid='153'
result:
[u'3770']
size:1
```

Find out more on starsql language [here](docs.macrodatalab.com).

## Administrative task

Users are provided with special command to perform adminstrative tasks such as
listing created objects, view object metadata, etc.  These commands are not
part of the query lanage.

To list created objects, execute

```bash
$ bosh> show [table|bo|...]
```

To see metadata in each object, execute

```bash
$ bosh> desc <object name>
```


## How to output results

After fetching desired results with Cross-Link, users can display the results
on standard output with the following commands

To output results stored in a local variable.

```bash
$ bosh>  print <variable name>
```
or directly print the results of a Cross-Link command::

```bash
$ bosh>  print CL_COMMAND
```
Cross-Link supports not only standard output, but also several file extensions including csv, xlsx, html.
choose expected style of output format by using corresponding suffix.
If the suffix is not supported, the results will be outputted as json format.


Output results directly to files, execute

```bash
$ bosh> CL_COMMAND >> [*.csv|*.html|*.xlsx|<file name>]
```

Open the output file right after the output file is generated, execute

```bash
$ bosh> CL_COMMAND >>@  [*.csv|*.html|*.xlsx|<file name>] 
```

