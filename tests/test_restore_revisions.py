"""The restorer must reject corrections made against a different baseline."""
import unittest,hashlib,json,copy,importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('restore_lots',Path(__file__).resolve().parents[1]/'restore_lots.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Revisions(unittest.TestCase):
 def setUp(self):
  self.old=[dict(id=322,tokens=[1,2],text='keep'),dict(id=323,tokens=[3,4],text='old')]
  self.revision=dict(id=323,old_tokens_sha256=hashlib.sha256(b'[3,4]').hexdigest(),old_text='old',new_selection=dict(id=323,tokens=[5,6],text='correct'),reason='Reviewed bilingual correction')
 def test_exact_correction_preserves_other_row_and_input(self):
  before=copy.deepcopy(self.old);out=m.merge_reviewed_revisions(self.old,[self.revision]);self.assertEqual(self.old,before);self.assertEqual(out[0],self.old[0]);self.assertEqual(out[1],self.revision['new_selection'])
 def test_empty_is_backwards_compatible(self):self.assertEqual(m.merge_reviewed_revisions(self.old,[]),self.old)
 def test_wrong_tokens(self):
  self.old[1]['tokens']=[8]
  with self.assertRaises(AssertionError):m.merge_reviewed_revisions(self.old,[self.revision])
 def test_wrong_text(self):
  self.old[1]['text']='other'
  with self.assertRaises(AssertionError):m.merge_reviewed_revisions(self.old,[self.revision])
 def test_unknown_id(self):
  self.revision['id']=9
  with self.assertRaises(AssertionError):m.merge_reviewed_revisions(self.old,[self.revision])
 def test_duplicate_revision(self):
  with self.assertRaises(AssertionError):m.merge_reviewed_revisions(self.old,[self.revision,self.revision])
 def test_wrong_replacement_id(self):
  self.revision['new_selection']['id']=322
  with self.assertRaises(AssertionError):m.merge_reviewed_revisions(self.old,[self.revision])
if __name__=='__main__':unittest.main()
