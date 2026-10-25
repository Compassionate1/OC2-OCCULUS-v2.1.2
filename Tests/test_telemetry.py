import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
class TelemetryTests(unittest.TestCase):
 def test_measured_success_and_failure(self):
  m=load('collect_telemetry');s=load('summarize_telemetry')
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'metrics.jsonl'
   self.assertEqual(m.measure(['python3','-c','pass'],f),0)
   self.assertEqual(m.measure(['python3','-c','raise SystemExit(7)'],f),7)
   records=[json.loads(line) for line in f.read_text().splitlines()]
   self.assertEqual([r['exit_code'] for r in records],[0,7]);self.assertTrue(all(r['duration_seconds']>=0 for r in records))
   summary=s.summarize(f);self.assertEqual(summary['observations'],2);self.assertEqual(summary['fail_count'],1)
 def test_empty(self):
  s=load('summarize_telemetry')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'empty';p.write_text('');self.assertEqual(s.summarize(p)['observations'],0)
if __name__=='__main__':unittest.main()
