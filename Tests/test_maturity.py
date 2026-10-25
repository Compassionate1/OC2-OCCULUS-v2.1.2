import unittest
from scripts.process_metrics import summarize,quantile
from scripts.experiment_analysis import analyze
from scripts.validate_science import validate,circular_error
class MaturityTests(unittest.TestCase):
 def test_quantile(self):self.assertEqual(quantile([1,2,3],.5),2)
 def test_empty(self):self.assertIsNone(quantile([],.9))
 def test_insufficient_data(self):self.assertFalse(summarize([{'phase':'test','duration_seconds':1,'exit_code':0}])['phases']['test']['baseline_eligible'])
 def test_eligible(self):self.assertTrue(summarize([{'phase':'test','duration_seconds':1,'exit_code':0}]*20)['phases']['test']['baseline_eligible'])
 def test_experiment_reproducible(self):self.assertEqual(analyze([10]*8,[8]*8),analyze([10]*8,[8]*8))
 def test_experiment_rejects_small(self):
  with self.assertRaises(ValueError):analyze([1],[2])
 def test_circular(self):self.assertEqual(circular_error(359,1),2)
 def test_science_accept(self):self.assertTrue(validate([{'truth_deg':1,'prediction_deg':2,'interval_halfwidth_deg':5}])['passed'])
 def test_science_reject(self):self.assertFalse(validate([{'truth_deg':1,'prediction_deg':100,'interval_halfwidth_deg':5}])['passed'])
if __name__=='__main__':unittest.main()
