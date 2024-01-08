import unittest

from src.loading.point.point import Point
from src.loading.point.places_manager import PlacesManager
from src.loading.point.points_update_info_resolver import PointsUpdateInfoResolver
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class TestLoadablePointsManager(unittest.TestCase):
    def setUp(self):
        volume_parameters = VolumeParameters(1000, 1000, 1000, 0)
        self._points_manager = PlacesManager(volume_parameters, PointsUpdateInfoResolver())

    def test_empty(self):
        expected_opening_points_n = 1
        expected_opening_point = Point(0, 0, 0)
        expected_closing_points = {Point(999, 999, 999)}

        self.assertEqual(len(self._points_manager.get_opening_points()), expected_opening_points_n)
        self.assertEqual(self._points_manager.get_opening_points()[0], expected_opening_point)
        self.assertEqual(self._points_manager.get_closing_points(expected_opening_point), expected_closing_points)
