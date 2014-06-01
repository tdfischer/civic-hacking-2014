#!/usr/bin/env python
from __future__ import absolute_import

import json
from json import JSONEncoder
from model import *

class JSONFormatter(object):
  def __init__(self, budget):
    self.budget = budget

  def generate(self):
    return json.dumps(self.budget, indent=2, cls=BudgetEncoder)

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
