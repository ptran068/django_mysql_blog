from django.test import TestCase, SimpleTestCase

# Create your tests here.

class SimpleTest(SimpleTestCase):
    def testHomePageStatus(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)