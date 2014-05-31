#!/usr/bin/env python
import xlrd
import sys
import json

book = xlrd.open_workbook(sys.argv[1], formatting_info=True)
sheet = book.sheet_by_name ("Expenditures")

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

print boldFormats

headerIdx = -1

for rownum in range(sheet.nrows):
  row = sheet.row(rownum)
  headerRun = 0
  for cell in row:
    if cell.xf_index in boldFormats and len(cell.value):
      headerRun += 1
  if headerRun >= 3:
    headerIdx = rownum
    print "Found headers at row", rownum
    break

headerRow = sheet.row(headerIdx)

columnMap = {}

for idx in range(len(headerRow)):
  headerCell = headerRow[idx]
  if len(headerCell.value):
    columnMap[idx] = headerCell.value

print "Got headers:", columnMap

alldata = []

for rownum in range(sheet.nrows):
  if rownum <= headerIdx:
    continue
  row = sheet.row(rownum)
  data = {}
  for columnidx,attrname in columnMap.iteritems():
    data[attrname] = row[columnidx].value
  if sum(map(lambda x:int(len(unicode(x)) > 0), data.itervalues())) < 5:
    continue
  alldata.append(data)
print json.dumps(alldata, indent=2)
