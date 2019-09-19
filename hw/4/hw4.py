from table import Table

class ZeroR(object):
  def __init__(self, cols):
    self.table = Table()
    self.table.read(cols)
    self.goalIndex = self.table.goals[0]
  
  def train(self, row):
    self.table.read(row)

  def classify(self, row):
    return row[self.goalIndex], self.table.cols[self.goalIndex].mode