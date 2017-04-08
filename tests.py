import unittest
from modules.navigation import haversine_distance
from modules.navigation import estimated_position
from modules.navigation import intersection
from modules.navigation import bearing
from modules.navigation import VMG
from modules.navigation import CMG
from modules.navigation import dist_bearing_to_gate
from modules.navigation import get_waypoint_list
from modules.navigation import get_waypoint_details

#1nm = 1.851999km

class Test_Navigation(unittest.TestCase):

    def setUp(self):
        pass

    def test_small_haversine_distance(self):
        self.assertEqual(2.993,
            round(
                haversine_distance(
                    (50.783777, -1.309129), (50.757939, -1.376420))
                ,3))

    def test_medium_haversine_distance(self):
        self.assertEqual(306.42,
            round(
                haversine_distance(
                    (50.783777, -1.309129), (51.200623, -9.385454))
                ,2))

    def test_large_haversine_distance(self):
        self.assertEqual(9312.1,
            round(
                haversine_distance(
                    (50.783777, -1.309129), (-53.310590, -140.166704))
                ,1))

    def test_estimated_position(self):
        self.assertEqual((50.7857, -1.3352),
                        estimated_position((50.7837, -1.3091),
                                           277,
                                           1,
                                           3600))

    def test_intersection(self):
        self.assertEqual((50.9076, 4.5086),
                         intersection((51.8853, 0.2545),
                                      108.55,
                                      (49.0034, 2.5735),
                                      32.44))

    def test_bearing(self):
        self.assertEqual(238.8030,
                         bearing((50.7837, -1.3091), 
                                 (50.7579, -1.3764)))

    def test_VMG(self):
        self.assertEqual(2.2943, VMG(4, 55, 0))

    def test_CMG(self):
        self.assertEqual(2.1976, CMG(5.2, 65, 0))


if __name__ == '__main__':
    unittest.main()
