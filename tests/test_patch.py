import json, tempfile, unittest
from pathlib import Path
from scripts.apply_patch import scan_resources, validate_translation

class PatchValidationTests(unittest.TestCase):
    def test_resource_scan(self):
        with tempfile.TemporaryDirectory() as td:
            res=Path(td)/'res'/'values'; res.mkdir(parents=True)
            (res/'strings.xml').write_text('<?xml version="1.0"?><resources><string name="hello">Hello %1$s</string><string-array name="days"><item>Mon</item><item>Tue</item></string-array><plurals name="items"><item quantity="one">%d item</item><item quantity="other">%d items</item></plurals></resources>',encoding='utf-8')
            found=scan_resources(Path(td)/'res')
            self.assertIn('hello',found['string'])
            self.assertEqual(found['string']['hello'],['Hello %1$s'])
            self.assertIn('days',found['string-array'])
            self.assertIn('items',found['plurals'])
    def test_string_placeholder_must_be_preserved(self):
        with self.assertRaises(RuntimeError):
            validate_translation('hello','Привет', 'strings',['Hello %1$s'])
    def test_valid_placeholder(self):
        validate_translation('hello','Привет, %1$s','strings',['Hello %1$s'])
    def test_russian_plural_requires_categories(self):
        with self.assertRaises(RuntimeError):
            validate_translation('items',{'one':'%d элемент','other':'%d элементов'},'plurals',['%d item\n%d items'])

if __name__=='__main__': unittest.main()
