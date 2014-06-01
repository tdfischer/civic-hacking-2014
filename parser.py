#!/usr/bin/env python

import xlrd
import sys
from formatter.json import JSONFormatter
from spreads import Spread
from model import *

class BudgetParser(object):
  def __init__(self, filename):
    super(BudgetParser, self).__init__()
    spread = Spread(filename)
    budget = BudgetData()

    data = spread.getTable('Sheet1',
        joins={
          'PROJECT': {'sheet': 'info', 'column': 'PROJECT'},
          'FUND': {'sheet': 'funds', 'column': 'FUND'}
        },
        tolerance=lambda x:len(str(x['F1']))>0)

    for p in data:
      print p
      proj = budget.getProject(p['PROJECT']['PROJECT'])
      fundData = p['FUND']
      alloc = proj.getAllocation(fundData['FUND'])
      alloc.forecast = p['FORECAST']
      alloc.budget = p['BUDGET']
      alloc.committed = p['COMMITTED']
      alloc.source.name = fundData['LABEL']
      alloc.source.type = fundData['TYPE']

    formatter = JSONFormatter(budget)
    print formatter.generate()
