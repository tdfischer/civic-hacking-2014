#!/usr/bin/env python
import xlrd
import sys
import json
from json import JSONEncoder

class BudgetEncoder(JSONEncoder):
  def default(self, o):
    if isinstance(o, BudgetData):
      return o.projects
    if isinstance(o, Project):
      return {
        'description': o.description,
        'sources': o.fundingSources
      }
    if isinstance(o, FundingSource):
      return {
        'committed': o.committed,
        'budget': o.budget,
        'forecast': o.forecast
      }
    return super(BudgetEncoder, self).default(o)

book = xlrd.open_workbook(sys.argv[1], formatting_info=True)
sheet = book.sheet_by_name ("Sheet1")

class BudgetData(object):
  def __init__(self):
    super(BudgetData, self).__init__()
    self.projects = {}

  def getProject(self, name):
    if name not in self.projects:
      self.projects[name] = Project(name)
    return self.projects[name]

class Project(object):
  def __init__(self, name):
    super(Project, self).__init__()
    self.name = name
    self.description = None
    self.wards = []
    self.limits = None
    self.fundingSources = {}

  def getSource(self, name):
    if name not in self.fundingSources:
      self.fundingSources[name] = FundingSource(name)
    return self.fundingSources[name]

class FundingSource(object):
  def __init__(self, name):
    super(FundingSource, self).__init__()
    self.name = name
    self.committed = 0
    self.budget = 0
    self.forecast = 0

formats = book.xf_list
fonts = book.font_list

boldFonts = []
boldFormats = []

for idx in range(len(fonts)):
  f = fonts[idx]
  if f.bold == 1:
    boldFonts.append(idx)

for idx in range(len(formats)):
  f = formats[idx]
  if f.font_index in boldFonts:
    boldFormats.append(idx)

headerIdx = -1

for rownum in range(sheet.nrows):
  row = sheet.row(rownum)
  headerRun = 0
  for cell in row:
    if cell.xf_index in boldFormats and len(cell.value):
      headerRun += 1
  if headerRun >= 3:
    headerIdx = rownum
    break

headerRow = sheet.row(headerIdx)

columnMap = {}

for idx in range(len(headerRow)):
  headerCell = headerRow[idx]
  if len(headerCell.value):
    columnMap[idx] = headerCell.value

budget = BudgetData()

rawProjects = []

for rownum in range(sheet.nrows):
  if rownum <= headerIdx:
    continue
  row = sheet.row(rownum)
  data = {}
  for columnidx,attrname in columnMap.iteritems():
    data[attrname] = row[columnidx].value
  if sum(map(lambda x:int(len(unicode(x)) > 0), data.itervalues())) < 5:
    continue
  rawProjects.append(data)

for p in rawProjects:
  proj = budget.getProject(p['PROJECT'])
  fund = proj.getSource(p['FUND'])
  fund.forecast = p['FORECAST']
  fund.budget = p['BUDGET']
  fund.committed = p['COMMITTED']

print json.dumps(budget, indent=2, cls=BudgetEncoder)
