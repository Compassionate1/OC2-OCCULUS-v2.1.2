import unittest
from bop5ii.model import Config,run,wrap,recognize
from bop5ii.validation import summarize,bootstrap_rmse

class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rows=run(Config(trajectories=12,steps=24))
    def test_repeatable(self):self.assertEqual(self.rows,run(Config(trajectories=12,steps=24)))
    def test_count(self):self.assertEqual(len(self.rows),288)
    def test_wrap(self):self.assertEqual(wrap(190),-170)
    def test_probability(self):
        for r in self.rows:
            self.assertTrue(0<=r.aperture_probability<=1)
            self.assertTrue(0<=r.arousal<=1)
            self.assertTrue(0<=r.recognition_confidence<=1)
    def test_recognition_templates(self):self.assertEqual(recognize((1.2,0))[0],'chirp')
    def test_occlusion(self):
        self.assertTrue(any(r.occluded for r in self.rows))
        self.assertTrue(all(not r.visible for r in self.rows if r.occluded))
    def test_holdout_metrics(self):
        m=summarize(self.rows)
        self.assertTrue(0<=m['recognition_macro_f1']<=1)
        self.assertEqual(len(bootstrap_rmse(self.rows,30)),2)
    def test_invalid_config(self):
        with self.assertRaises(AssertionError):Config(occlusion_probability=2).validate()
if __name__=='__main__':unittest.main()
