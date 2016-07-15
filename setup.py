from setuptools import setup, find_packages

setup(
    name='bosh',
    version='0.2.19',
    packages=find_packages(),

    install_requires=[
	'requests',
        'pyparsing',
        'openpyxl',
	'bosh-dumpRes',
	'bosh-db2bt'
    ],

    entry_points = {
        'console_scripts': [
            'bosh = bosh.bosh:main'
        ]
    },

    author='MacroData Inc',
    author_email='info@macrodatalab.com',
    description='BigObject service command line tool',
    license='Apache 2.0',
    keywords=[
        'bigobject',
        'macrodata',
        'analytics',
        'command line tool',
    ],
    url='https://github.com/bigobject-inc/bosh.git',

    zip_safe=False
)
