# BOSH - a BigObject shell

BigObject service provides storage and analytic computation for your data.
These feature endpoints are made available through BigObject query language,
**boql**.  The language are divided into two feature sets, with a single admin
control for list and get metadata opertions.

Refer to the full documentation [here](docs.bigobject.io/)

## Getting BigObject service

We recommend you provision a BigObject service through
[Docker Hub](https://registry.hub.docker.com/u/macrodata/bigobject/).  Other options available through custom
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

