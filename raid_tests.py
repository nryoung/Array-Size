import raid
import unittest

class RaidTestCase(unittest.TestCase):
    """
    Tests the following functions for floats and expected data
    GET
    POST
    CalcArraySize
    """
    
    def setUp(self):
       raid.app.config['TESTING'] = True
       self.app = raid.app.test_client()

    def postRaid(self, num_disks, sod, raid_type):
        return self.app.post('/', data=dict(
            num_disks = num_disks,
            sod = sod,
            raid_type = raid_type
            ))

    def testCalcArraySize(self):
        rv = raid.calc_array_size(10, 100, 4)
        self.assertIsInstance(rv['array_size'], float)
        self.assertIsInstance(rv['ads'], float)

    def testGET(self):
        resp = self.app.get('/')
        self.assertIn('<h1><a href="/">ArraySize</a></h1>', resp.data)

    def testPOST(self):
        resp = self.postRaid(10, 100, 4)
        self.assertIn('<h2>Your array:</h2>', resp.data)
        
       
if __name__ == '__main__':
    unittest.main() 
