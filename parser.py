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

    for p in spread.getTable('Sheet1'):
      proj = budget.getProject(p['PROJECT'])
      fund = proj.getAllocation(p['FUND'])
      fund.forecast = p['FORECAST']
      fund.budget = p['BUDGET']
      fund.committed = p['COMMITTED']

    formatter = JSONFormatter(budget)
    print formatter.generate()
