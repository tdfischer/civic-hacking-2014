import xlrd

class Table(list):
  def __init__(self):
    super(Table, self).__init__()
    self.headers = HeaderSet()

class HeaderSet(dict):
  def __init__(self):
    super(HeaderSet, self).__init__()
    self.source_row = 0

class Spread(object):
  def __init__(self, sheetfile):
    super(Spread, self).__init__()
    self.book = xlrd.open_workbook(sheetfile, formatting_info=True)

  def findHeaders(self, sheet, start=0, end=-1):
    sheet = self.book.sheet_by_name (sheet)

    bestRow = -1
    bestRun = 0
    if end == -1:
      end = sheet.nrows
    for rownum in  range(start, end):
      row = sheet.row(rownum)
      headerRun = 0
      for cell in row:
        if len(unicode(cell.value)):
          headerRun += 1
          if headerRun > bestRun:
            bestRow = rownum
            bestRun = headerRun
        else:
          headerRun = 0

    headerRow = sheet.row(bestRow)
    columnMap = HeaderSet()

    for idx in range(len(headerRow)):
      headerCell = headerRow[idx]
      if len(headerCell.value):
        columnMap[idx] = headerCell.value
    columnMap.source_row = bestRow
    return columnMap

  def getTable(self, sheet, joins={}, start=-1, end=-1, tolerance=2):
    headers = self.findHeaders(sheet, start, end)
    sheet = self.book.sheet_by_name(sheet)

    if isinstance(tolerance, int):
      meetsTolerance = lambda x:sum(map(lambda y:int(len(unicode(y)) > 0), x.itervalues())) < tolerance
    else:
      assert(callable(tolerance))
      meetsTolerance = tolerance

    if end == -1:
      end = sheet.nrows

    if start == -1:
      start = headers.source_row+1

    data = Table()
    data.headers = headers

    joinTables = []
    for joinCol, joinData in joins.iteritems():
      joinTables.append({
        'table': self.getTable(joinData['sheet']),
        'dst': joinCol,
        'src': joinData['column']
      })

    if tolerance < 1:
      tolerance = len(headers) * tolerance

    for rownum in range(start, end):
      row = sheet.row(rownum)
      rowdata = {}
      for columnidx,attrname in headers.iteritems():
        rowdata[attrname] = row[columnidx].value
      if not meetsTolerance(rowdata):
        continue
      else:
        for join in joinTables:
          table = join['table']
          src = join['src']
          dst = join['dst']
          matchedRow = None
          for joinRow in table:
            if joinRow[dst] == rowdata[src]:
              matchedRow = joinRow
              break
          if matchedRow:
            rowdata[src] = matchedRow
          else:
            #print "Cannot join", joinRow[dst], rowdata[src]
            nullData = {}
            for h in table.headers.itervalues():
              nullData[h] = None
            nullData[src] = rowdata[src]
            rowdata[src] = nullData
        data.append(rowdata)

    return data
