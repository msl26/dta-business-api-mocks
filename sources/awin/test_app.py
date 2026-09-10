"""Tests for the Awin mock API."""

import unittest

from sources.awin.main import app


class AwinMockTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.params = {
            "dateType": "transaction",
            "startDate": "2026-08-30T00:00:00",
            "endDate": "2026-08-30T23:59:59",
            "timezone": "Europe/London",
            "page": 1,
            "pageSize": 10000,
        }
        self.headers = {"Authorization": "Bearer dummy-awin-oauth-token"}

    def test_returns_transactions(self):
        response = self.client.get(
            "/advertisers/123456/transactions/",
            query_string=self.params,
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 3)

    def test_requires_bearer_token(self):
        response = self.client.get(
            "/advertisers/123456/transactions/",
            query_string=self.params,
        )

        self.assertEqual(response.status_code, 401)

    def test_filters_by_validation_date(self):
        params = dict(self.params, dateType="validation")
        response = self.client.get(
            "/advertisers/123456/transactions/",
            query_string=params,
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([record["id"] for record in response.get_json()], [233982939])


if __name__ == "__main__":
    unittest.main()
