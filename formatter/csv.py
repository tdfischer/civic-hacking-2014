#!/usr/bin/env python
from __future__ import absolute_import

import csv
import io
import sys
import time
from model import *

class Formatter(object):
  def __init__(self, budget):
    self.budget = budget

  def generate(self):
    output = io.BytesIO()
    writer = csv.writer(output)

    writer.writerow(['FUNDING SOURCES ======================='])
    writer.writerow(['Symbol', 'Name', 'Type'])
    for fund_name, funding_source in self.budget.funds.iteritems():
      writer.writerow([funding_source.symbol, funding_source.name, funding_source.type])

    writer.writerow('')
    writer.writerow(['PROJECTS =============================='])
    writer.writerow(['Project Name', 'Description', 'Limits', 'Wards'])
    for project, data in self.budget.projects.iteritems():
      writer.writerow([project.encode('utf-8'), data.description, data.limits, data.wards])

    # writer.writerow('')
    # writer.writerow(['PROJECT ALLOCATIONS ==================='])
    # writer.writerow(['Project Name', 'Description', 'Limits', 'Wards'])
    # for project, data in self.budget.projects.iteritems():
    #   writer.writerow([project.encode('utf-8'), data.description, data.limits, data.wards])

    return output.getvalue()
