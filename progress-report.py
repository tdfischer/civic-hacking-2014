#!/usr/bin/env python
import xlrd
import sys
import json
from json import JSONEncoder
from spreads import Spread

class BudgetEncoder(JSONEncoder):
  def default(self, o):
    if isinstance(o, BudgetData):
      return {
        'projects': o.projects,
        'funds': o.funds
      }
    if isinstance(o, Project):
      return {
        'description': o.description,
        'allocations': o.allocations
      }
    if isinstance(o, FundingAllocation):
      return {
        'committed': o.committed,
        'budget': o.budget,
        'forecast': o.forecast
      }
    if isinstance(o, FundingSource):
      return {  
        'name': o.name
      }
    return super(BudgetEncoder, self).default(o)

class BudgetData(object):
  def __init__(self):
    super(BudgetData, self).__init__()
    self.projects = {}
    self.funds = {}

  def getProject(self, name):
    if name not in self.projects:
      self.projects[name] = Project(self, name)
    return self.projects[name]

  def getFund(self, symbol):
    if symbol not in self.funds:
      self.funds[symbol] = FundingSource(symbol)
    return self.funds[symbol]

class Project(object):
  def __init__(self, budget, name):
    super(Project, self).__init__()
    self.budget = budget
    self.name = name
    self.description = None
    self.wards = []
    self.limits = None
    self.allocations = {}

  def getAllocation(self, symbol):
    source = self.budget.getFund(symbol)
    if symbol not in self.allocations:
      self.allocations[symbol] = FundingAllocation(source)
    return self.allocations[symbol]

class FundingAllocation(object):
  def __init__(self, source):
    self.source = source
    self.committed = 0
    self.budget = 0
    self.forecast = 0

class FundingSource(object):
  def __init__(self, symbol):
    super(FundingSource, self).__init__()
    self.symbol = symbol
    self.name = None

spread = Spread(sys.argv[1])
budget = BudgetData()

for p in spread.getTable('Sheet1'):
  proj = budget.getProject(p['PROJECT'])
  fund = proj.getAllocation(p['FUND'])
  fund.forecast = p['FORECAST']
  fund.budget = p['BUDGET']
  fund.committed = p['COMMITTED']

print json.dumps(budget, indent=2, cls=BudgetEncoder)
