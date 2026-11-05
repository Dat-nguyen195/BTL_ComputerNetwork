#!/usr/bin/env python3
"""Regression checks against corrupted or falsely labelled MPLS evidence."""
import json,shutil,struct,tempfile,unittest
from pathlib import Path
from check_mpls import ROOT,frames,check_run

class EvidenceTests(unittest.TestCase):
 def fixture(self,tmp):
  base=ROOT/'test_results/mpls/validated'
  for name in ['results.json','mpls.pcap']:shutil.copy2(base/name,Path(tmp)/name)
  return Path(tmp)
 def test_real_capture_contains_two_labels_and_return(self):
  data=frames(ROOT/'test_results/mpls/validated/mpls.pcap')
  self.assertTrue(any(len(x['labels'])==2 for x in data))
  self.assertTrue(any(x['src']=='10.10.10.10' for x in data))
 def test_truncated_capture_is_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=self.fixture(tmp)/'mpls.pcap';p.write_bytes(p.read_bytes()[:-1])
   with self.assertRaises(AssertionError):frames(p)
 def test_plain_ip_is_not_mpls(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=self.fixture(tmp)/'mpls.pcap';data=bytearray(p.read_bytes());endian='<' if data[:4]==b'\xd4\xc3\xb2\xa1' else '>'
   length=struct.unpack(endian+'I',data[32:36])[0];data=data[:40+length];data[52:54]=b'\x08\x00';p.write_bytes(data)
   self.assertEqual(frames(p),[])
 def test_pass_label_does_not_override_failed_command(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=self.fixture(tmp);p=d/'results.json';r=json.loads(p.read_text());next(x for x in r['cases'] if x['id']=='MPLS-INTERNET-Main')['returncode']=7;p.write_text(json.dumps(r))
   with self.assertRaises(AssertionError):check_run(d)
if __name__=='__main__':unittest.main()
