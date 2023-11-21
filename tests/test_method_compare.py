import unittest
import random
from app import StandardLoan, PriorityQueue, MethodCompare

class PriorityQueueTest(unittest.TestCase):
  def setUp(self):
    
    self.budget = 750
    self.loans = [
      StandardLoan(3245.65, 4.41, title="2014", term=36),
      StandardLoan(12002.91, 3.61, title="2013", term=120),
      StandardLoan(2481.30, 6.1, title="2012", term=60),
      StandardLoan(5930.42, 6.1, title="2011", term=120)
    ]

    # Start our primary queue and display
    self.priority_queue = PriorityQueue(self.loans, self.budget, title="Test Loans")
    # Get a MethodCompare obj
    minimum = 'min'
    minimum = 'int'
    minimum = 'avg'

    self.method_compare = MethodCompare([
      self.priority_queue.avalanche(minimum),
      self.priority_queue.cascade(minimum),
      self.priority_queue.blizzard(minimum),
      self.priority_queue.ice_slide(minimum),
      self.priority_queue.snowball(minimum)
    ])

  def test_interest_goal(self):
    self.method_compare.order_by('interest')
    self.assertEqual(self.method_compare.grid[0].title, 'Test Loans(avalanche)')
    self.assertEqual(self.method_compare.grid[1].title, 'Test Loans(cascade)')
    self.assertEqual(self.method_compare.grid[2].title, 'Test Loans(blizzard)')
    self.assertEqual(self.method_compare.grid[3].title, 'Test Loans(ice_slide)')
    self.assertEqual(self.method_compare.grid[4].title, 'Test Loans(snowball)')

  def test_time_goal(self):
    self.method_compare.order_by('time')
    self.assertEqual(self.method_compare.grid[0].title, 'Test Loans(avalanche)')
    self.assertEqual(self.method_compare.grid[1].title, 'Test Loans(cascade)')
    self.assertEqual(self.method_compare.grid[2].title, 'Test Loans(blizzard)')
    self.assertEqual(self.method_compare.grid[3].title, 'Test Loans(ice_slide)')
    self.assertEqual(self.method_compare.grid[4].title, 'Test Loans(snowball)')

  def test_fewest_payments_goal(self):
    self.method_compare.order_by('num_p')
    self.assertEqual(self.method_compare.grid[0].title, 'Test Loans(avalanche)')
    self.assertEqual(self.method_compare.grid[1].title, 'Test Loans(cascade)')
    self.assertEqual(self.method_compare.grid[2].title, 'Test Loans(blizzard)')
    self.assertEqual(self.method_compare.grid[3].title, 'Test Loans(ice_slide)')
    self.assertEqual(self.method_compare.grid[4].title, 'Test Loans(snowball)')

if __name__ == "main":
  unittest.main()
