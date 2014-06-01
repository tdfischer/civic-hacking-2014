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
    self.type = None
