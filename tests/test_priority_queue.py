import unittest
import random
from app import StandardLoan, PriorityQueue, MethodCompare

class PriorityQueueTest(unittest.TestCase):
  def setUp(self):

    # Random example
    # self.budget = random.uniform(800, 2000)
    # self.loans = [
    #   StandardLoan(
    #     random.uniform(2000, 25000),
    #     random.uniform(1, 12),
    #     term=random.randint(12, 360)
    #     ) for i in range(n)
    # ]

    # Specific example
    self.budget = 1200
    self.loans = [
      StandardLoan(2406.65, 4.41, title="2014", term=120),
      StandardLoan(2472.91, 3.61, title="2013", term=120),
      StandardLoan(6282.30, 6.1, title="2012", term=120),
      StandardLoan(5930.42, 6.1, title="2011", term=120)
    ]

    # Start our primary queue and display
    self.priority_queue = PriorityQueue(self.loans, self.budget, title="Test Loans")
  
  def test_avalanche(self):
    avalanche = self.priority_queue.avalanche()
    avalanche.display_info()
    self.assertEqual(avalanche.get_duration(), StandardLoan.Dec(16))
    self.assertEqual(avalanche.get_num_payments(), StandardLoan.Dec(48))
    self.assertEqual(avalanche.get_interest_paid(), StandardLoan.Dec(600.42))
    self.assertEqual(avalanche.get_percent_principal(), StandardLoan.Dec(96.61))
  
  def test_cascade(self):
    cascade = self.priority_queue.cascade()
    cascade.display_info()
    self.assertEqual(cascade.get_duration(), StandardLoan.Dec(16))
    self.assertEqual(cascade.get_num_payments(), StandardLoan.Dec(53))
    self.assertEqual(cascade.get_interest_paid(), StandardLoan.Dec(641.56))
    self.assertEqual(cascade.get_percent_principal(), StandardLoan.Dec(96.38))

  def test_ice_slide(self):
    ice_slide = self.priority_queue.ice_slide()
    ice_slide.display_info()
    self.assertEqual(ice_slide.get_duration(), StandardLoan.Dec(16))
    self.assertEqual(ice_slide.get_num_payments(), StandardLoan.Dec(61))
    self.assertEqual(ice_slide.get_interest_paid(), StandardLoan.Dec(614.53))
    self.assertEqual(ice_slide.get_percent_principal(), StandardLoan.Dec(96.53))

  def test_blizzard(self):
    blizzard = self.priority_queue.blizzard()
    blizzard.display_info()
    self.assertEqual(blizzard.get_duration(), StandardLoan.Dec(17))
    self.assertEqual(blizzard.get_num_payments(), StandardLoan.Dec(65))
    self.assertEqual(blizzard.get_interest_paid(), StandardLoan.Dec(589.93))
    self.assertEqual(blizzard.get_percent_principal(), StandardLoan.Dec(96.66))

  def test_snowball(self):
    snowball = self.priority_queue.snowball()
    snowball.display_info()
    self.assertEqual(snowball.get_duration(), StandardLoan.Dec(17))
    self.assertEqual(snowball.get_num_payments(), StandardLoan.Dec(38))
    self.assertEqual(snowball.get_interest_paid(), StandardLoan.Dec(775.56))
    self.assertEqual(snowball.get_percent_principal(), StandardLoan.Dec(95.66))

if __name__ == "main":
  unittest.main()
