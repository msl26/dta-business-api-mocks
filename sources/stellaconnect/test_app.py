"""Tests for the StellaConnect mock API."""

from datetime import datetime, timedelta, timezone
import unittest

from sources.stellaconnect.main import app


class StellaConnectMockTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_returns_historical_backload_record(self):
        response = self.client.get(
            "/surveys",
            query_string={"created_at_gte": "2023-01-15", "created_at_lte": "2023-01-15"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([record["sequence_id"] for record in response.get_json()], [301])

    def test_returns_recent_record(self):
        yesterday = (datetime.now(timezone.utc).date() - timedelta(days=1)).isoformat()
        response = self.client.get(
            "/surveys",
            query_string={"created_at_gte": yesterday, "created_at_lte": yesterday},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([record["sequence_id"] for record in response.get_json()], [302])

    def test_returns_empty_without_date_filter(self):
        response = self.client.get("/surveys")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])


if __name__ == "__main__":
    unittest.main()
