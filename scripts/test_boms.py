import json,subprocess,sys,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class TestBOMs(unittest.TestCase):
 def test_generated_boms(self):
  subprocess.run([sys.executable,str(R/'scripts/generate_boms.py')],check=True)
  s=json.loads((R/'compliance/sbom.cyclonedx.json').read_text());self.assertEqual(s['specVersion'],'1.5');self.assertGreaterEqual(len(s['components']),10)
  p=json.loads((R/'compliance/sbom.spdx.json').read_text());self.assertEqual(p['spdxVersion'],'SPDX-2.3')
  c=json.loads((R/'compliance/cbom.cyclonedx.json').read_text());self.assertEqual(c['specVersion'],'1.6');self.assertTrue(any('Ed25519' in x['name'] for x in c['components']))
  h=json.loads((R/'compliance/source-hashes.json').read_text());self.assertGreater(len(h['files']),30)
if __name__=='__main__': unittest.main()
