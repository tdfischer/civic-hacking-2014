# Progress Report Parser

Development done for the City of Akron as part of the of 2014 National Day of Civic Hacking

### Installation

The parser is written in [Python](https://www.python.org/download/), which
you'll need to have installed on your machined to run the application.

You can then install `pip`: http://pip.readthedocs.org/en/latest/installing.html

Finally, you can install the dependencies for the project by running:

    pip install -r requirements.txt


### Running the App

From the command line, you can run:

    python parser.py path/to/file.xls > file/to/save.json

To change the format of the output file, you can pass an outputter. For example,
to export the data in CSV format you can run:

    python parser.py --format cvs path/to/file.xls > file/to/save.csv

You can get information on what options are available by running:

    python parse.py --help

#### CSV Export

*Warning*: we ran out of time on the CSV output format and functionality for
outputting the project allocations to a separate section needs to still be
completed.

We output data to the console by default so it can be output to a file. Since
the CSV data crosses multiple tables and all output done at once, we split the
different table information with delimeters and header rows in the output.


### Sample data

Sample data from the City of Akron's 2009, 2010, and 2011 fiscal years are in sample-data/
