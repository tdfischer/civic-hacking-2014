#!/usr/bin/env python

from argparse import ArgumentParser
from parser import BudgetParser

parser = ArgumentParser(description='Format a progress report into a specific output file format.')
parser.add_argument('filename', help='the excel file to parse')
parser.add_argument('-f', '--format', default='json', dest='format',
                  help='format of output file, defaults to "json"', metavar='FORMAT')

args = parser.parse_args()
parser = BudgetParser(args.filename, args.format)
