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

You can get information on what options are available by running:

    python parse.py --help


### Sample data

Sample data from the City of Akron's 2009, 2010, and 2011 fiscal years are in sample-data/
