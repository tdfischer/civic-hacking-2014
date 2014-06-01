import xlrd

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

  def getTable(self, sheet, start=-10, end=-1, tolerance=2):
    headers = self.findHeaders(sheet, start, end)
    sheet = self.book.sheet_by_name(sheet)

    if end == -1:
      end = sheet.nrows

    if start == -1:
      start = headers.source_row+1

    data = []

    if tolerance < 1:
      tolerance = len(headers) * tolerance

    for rownum in range(start, end):
      row = sheet.row(rownum)
      rowdata = {}
      for columnidx,attrname in headers.iteritems():
        rowdata[attrname] = row[columnidx].value
      if sum(map(lambda x:int(len(unicode(x)) > 0), rowdata.itervalues())) < tolerance:
        continue
      else:
        data.append(rowdata)

    return data
