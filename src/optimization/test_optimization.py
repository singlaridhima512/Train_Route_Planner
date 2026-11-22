
"""Unit tests for optimization metrics and ranking."""

import unittest

from .route_metrics import (
    total_travel_time,
    total_distance,
    count_transfers,
    route_metrics,
)
from .route_ranking import rank_routes


class RouteMetricsTests(unittest.TestCase):

    def setUp(self):
        self.route = {
            "route_id": "sample",
            "legs": [
                {
                    "train_id": "T1",
                    "travel_time_minutes": 40,
                    "distance_km": 25
                },
                {
                    "train_id": "T1",
                    "travel_time_minutes": 30,
                    "distance_km": 20
                },
                {
                    "train_id": "T2",
                    "travel_time_minutes": 15,
                    "distance_km": 10
                },
            ],
        }

    def test_total_travel_time(self):
        self.assertEqual(total_travel_time(self.route), 85)

    def test_total_distance(self):
        self.assertEqual(total_distance(self.route), 55)

    def test_count_transfers(self):
        self.assertEqual(count_transfers(self.route), 1)

    def test_route_metrics(self):
        expected = {
            "total_travel_time": 85,
            "total_distance": 55,
            "count_transfers": 1,
            "number_of_legs": 3,
        }

        self.assertEqual(route_metrics(self.route), expected)

    def test_negative_duration_rejected(self):
        bad_route = {
            "legs": [
                {
                    "train_id": "A",
                    "travel_time_minutes": -5
                }
            ]
        }

        with self.assertRaises(ValueError):
            total_travel_time(bad_route)


class RouteRankingTests(unittest.TestCase):

    def test_fastest_route_ranks_first_with_default_weights(self):

        routes = [
            {
                "route_id": "slow",
                "legs": [
                    {
                        "train_id": "A",
                        "travel_time_minutes": 120,
                        "distance_km": 100
                    }
                ]
            },
            {
                "route_id": "fast",
                "legs": [
                    {
                        "train_id": "B",
                        "travel_time_minutes": 60,
                        "distance_km": 80
                    }
                ]
            }
        ]

        ranked = rank_routes(routes)

        self.assertEqual(
            ranked[0]["route"]["route_id"],
            "fast"
        )

        self.assertLess(
            ranked[0]["score"],
            ranked[1]["score"]
        )

    def test_empty_routes(self):
        self.assertEqual(rank_routes([]), [])

    def test_invalid_weights_rejected(self):

        routes = [
            {
                "legs": [
                    {
                        "train_id": "A",
                        "travel_time_minutes": 10,
                        "distance_km": 5
                    }
                ]
            }
        ]

        with self.assertRaises(ValueError):
            rank_routes(
                routes,
                {
                    "travel_time": -1,
                    "transfers": 0.3,
                    "distance": 0.1
                }
            )


if __name__ == "__main__":
    unittest.main()
