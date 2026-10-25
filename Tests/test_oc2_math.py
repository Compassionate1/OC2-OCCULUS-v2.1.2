import math,unittest,statistics
from services.simulator import simulate,circular_error
from services.contracts import new_event,validate_event
class MathTests(unittest.TestCase):
 def test_circular_wrap(self):
  self.assertEqual(circular_error(359,1),-2)
  self.assertEqual(circular_error(1,359),2)
 def test_determinism(self):
  def projection():return [(e['event_type'],e.get('bearing_deg'),e['payload']) for e in simulate(17,20,2)]
  self.assertEqual(projection(),projection())
 def test_multiple_trajectories(self):
  e=list(simulate(2026,100,4));self.assertEqual(len(set(x['payload']['track_id'] for x in e)),4)
  self.assertGreater(len([x for x in e if x['event_type']=='audio']),50)
 def test_occlusion_and_snr(self):
  e=list(simulate(2026,200,5));self.assertTrue(any(x['payload'].get('occluded') for x in e));self.assertGreater(statistics.pstdev([x['payload']['snr_db'] for x in e if x['event_type']=='audio']),5)
 def test_angular_rmse_and_coverage(self):
  e=[x for x in simulate(2026,300,4) if x['event_type']=='visual'];errors=[circular_error(x['bearing_deg'],x['payload']['ground_truth_deg']) for x in e]
  rmse=math.sqrt(statistics.mean(z*z for z in errors));coverage=sum(abs(z)<=1.96*1.8 for z in errors)/len(errors)
  self.assertLess(rmse,3.0);self.assertGreater(coverage,.90);self.assertLess(coverage,.99)
 def test_validation(self):
  e=new_event('sim','simulation','audio',{'a':1},confidence=.5);self.assertEqual(validate_event(e),e)
  e['confidence']=1.2
  with self.assertRaises(ValueError):validate_event(e)
 def test_no_nonfinite(self):
  e=new_event('sim','simulation','audio',{},bearing_deg=0);e['bearing_deg']=float('nan')
  with self.assertRaises(ValueError):validate_event(e)
if __name__=='__main__':unittest.main()
