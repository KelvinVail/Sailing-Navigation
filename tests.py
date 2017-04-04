import unittest
from modules.navigation import haversine_distance


class Test_Navigation(unittest.TestCase):

    def setUp(self):
        pass

    def test_small_haversine_distance(self):
        self.assertEqual(
            round(
                haversine_distance(
                    (50.783777, -1.309129), (50.757939, -1.376420))
                ,3)
            , 2.993)

    def test_medium_haversine_distance(self):
        self.assertEqual(
            round(
                haversine_distance(
                    (50.783777, -1.309129), (51.200623, -9.385454))
                ,2)
            , 306.42)

    def test_large_haversine_distance(self):
        self.assertEqual(
            round(
                haversine_distance(
                    (50.783777, -1.309129), (-53.310590, -140.166704))
                ,1)
            , 9312.1)

if __name__ == '__main__':
    unittest.main()
