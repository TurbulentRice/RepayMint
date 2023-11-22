######################################################
#   METHOD COMPARE OBJECT
#   Container for multiple PriorityQueues
######################################################
class MethodCompare:
  def __init__(self, q_list):
    # List of PriorityQueues
    self.grid = q_list

  def top(self):
    return self.grid[0]

  def order_by(self, goal):
    if goal == 'interest':
      self.grid.sort(key=lambda q: q.get_interest_paid())
    elif goal == 'time':
      self.grid.sort(key=lambda q: q.get_duration())
    elif goal == 'num_p':
      self.grid.sort(key=lambda q: q.get_num_payments())

  def all_complete(self):
    return all([q.is_complete() for q in self.grid])

  def display_info(self, **kwargs):
    for q in self.grid:
      q.display_info(**kwargs)
