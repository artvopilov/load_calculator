import unittest

from src.loading.point.point import Point
from src.loading.point.places_manager import PlacesManager
from src.loading.point.points_update_info_resolver import PointsUpdateInfoResolver
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class TestLoadablePointsManager(unittest.TestCase):
    def setUp(self):
        volume_parameters = VolumeParameters(1000, 1000, 1000, 0)
        self._places_manager = PlacesManager(volume_parameters, PointsUpdateInfoResolver())

    def test_empty(self):
        expected_places = {Point(0, 0, 0): {Point(999, 999, 999)}}

        self.assertEqual(len(self._places_manager.get_opening_points()), len(expected_places))
        for opening_p, closing_ps in self._places_manager.places.items():
            self.assertTrue(opening_p in expected_places)
            self.assertSetEqual(closing_ps, expected_places[opening_p])

    def test_one_corner_shipment(self):
        self._places_manager.update(Point(0, 0, 0), Point(2, 2, 2), True)

        expected_places = {
            Point(0, 0, 3): {Point(2, 2, 999)},
            Point(0, 3, 0): {Point(999, 999, 999)},
            Point(3, 0, 0): {Point(999, 999, 999)},
        }

        self.assertEqual(len(self._places_manager.get_opening_points()), len(expected_places))
        for opening_p, closing_ps in self._places_manager.places.items():
            self.assertTrue(opening_p in expected_places)
            self.assertSetEqual(closing_ps, expected_places[opening_p])

    def test_two_corner_shipments(self):
        self._places_manager.update(Point(0, 0, 0), Point(2, 2, 2), True)
        self._places_manager.update(Point(3, 0, 0), Point(5, 2, 2), True)

        expected_places = {
            Point(0, 0, 3): {Point(5, 2, 999)},
            Point(0, 3, 0): {Point(999, 999, 999)},
            Point(6, 0, 0): {Point(999, 999, 999)},
        }

        self.assertEqual(len(self._places_manager.get_opening_points()), len(expected_places))
        for opening_p, closing_ps in self._places_manager.places.items():
            self.assertTrue(opening_p in expected_places)
            self.assertSetEqual(closing_ps, expected_places[opening_p])

    def test_three_corner_shipments(self):
        self._places_manager.update(Point(0, 0, 0), Point(2, 2, 2), True)
        self._places_manager.update(Point(3, 0, 0), Point(5, 2, 2), True)
        self._places_manager.update(Point(0, 3, 0), Point(2, 5, 2), True)

        expected_places = {
            Point(0, 0, 3): {Point(5, 2, 999), Point(2, 5, 999)},
            Point(0, 6, 0): {Point(999, 999, 999)},
            Point(6, 0, 0): {Point(999, 999, 999)},
            Point(3, 3, 0): {Point(999, 999, 999)},
        }

        self.assertEqual(len(self._places_manager.get_opening_points()), len(expected_places))
        for opening_p, closing_ps in self._places_manager.places.items():
            self.assertTrue(opening_p in expected_places)
            self.assertSetEqual(closing_ps, expected_places[opening_p])

    def test_three_corner_shipments_no_stack(self):
        self._places_manager.update(Point(0, 0, 0), Point(2, 2, 2), False)
        self._places_manager.update(Point(3, 0, 0), Point(5, 2, 2), False)
        self._places_manager.update(Point(0, 3, 0), Point(2, 5, 2), False)

        expected_places = {
            Point(0, 6, 0): {Point(999, 999, 999)},
            Point(6, 0, 0): {Point(999, 999, 999)},
            Point(3, 3, 0): {Point(999, 999, 999)},
        }

        self.assertEqual(len(self._places_manager.get_opening_points()), len(expected_places))
        for opening_p, closing_ps in self._places_manager.places.items():
            self.assertTrue(opening_p in expected_places)
            self.assertSetEqual(closing_ps, expected_places[opening_p])

    def test_three_corner_shipments_one_without_stack(self):
        self._places_manager.update(Point(0, 0, 0), Point(2, 2, 2), True)
        self._places_manager.update(Point(3, 0, 0), Point(5, 2, 2), True)
        self._places_manager.update(Point(0, 3, 0), Point(2, 5, 2), False)

        expected_places = {
            Point(0, 0, 3): {Point(5, 2, 999)},
            Point(0, 6, 0): {Point(999, 999, 999)},
            Point(6, 0, 0): {Point(999, 999, 999)},
            Point(3, 3, 0): {Point(999, 999, 999)},
        }

        self.assertEqual(len(self._places_manager.get_opening_points()), len(expected_places))
        for opening_p, closing_ps in self._places_manager.places.items():
            self.assertTrue(opening_p in expected_places)
            self.assertSetEqual(closing_ps, expected_places[opening_p])
