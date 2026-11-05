import unittest
from app import login

class LoginTests(unittest.TestCase):
    def test_valid_credentials(self):
        for mode in ('vulnerable','fixed'):
            self.assertTrue(login(mode,'admin','AdminDemo42!')['accepted'])
    def test_wrong_password(self):
        for mode in ('vulnerable','fixed'):
            self.assertFalse(login(mode,'admin','wrong')['accepted'])
    def test_injection_bypasses_only_vulnerable(self):
        for mode in ('vulnerable','fixed'):
            result=login(mode,"admin' -- ",'wrong')
            self.assertEqual(result['accepted'],mode=='vulnerable')
            if mode=='vulnerable': self.assertEqual(result['user']['name'],'admin')
    def test_unknown_and_empty(self):
        for mode in ('vulnerable','fixed'):
            for name in ('nobody',''):
                self.assertFalse(login(mode,name,'')['accepted'])
    def test_quote_is_data_in_fixed(self):
        result=login('fixed',"O'Brien",'anything')
        self.assertFalse(result['accepted'])
        self.assertIsNone(result['error'])
    def test_database_resets(self):
        login('vulnerable',"admin' -- ",'x')
        self.assertTrue(login('fixed','student','StudyDemo42!')['accepted'])
    def test_invalid_mode(self):
        with self.assertRaises(ValueError): login('other','a','b')

if __name__=='__main__': unittest.main()
