"""Mock Awin Transactions API for development and integration testing."""

from datetime import datetime

from flask import Flask, jsonify, request

from shared.response_headers import build_json_response_headers

app = Flask(__name__)

ADVERTISER_ID = 123456

TRANSACTIONS = [
    {
        "id": 233982938,
        "advertiserId": ADVERTISER_ID,
        "publisherId": 231221,
        "siteName": "Broadband Choices",
        "commissionStatus": "pending",
        "commissionAmount": {"amount": 90.75, "currency": "GBP"},
        "saleAmount": {"amount": 1, "currency": "GBP"},
        "transactionDate": "2026-08-30T00:01:00",
        "validationDate": None,
        "orderRef": "mock-order-001",
    },
    {
        "id": 2234324324,
        "advertiserId": ADVERTISER_ID,
        "publisherId": 231332,
        "siteName": "Cardlytics",
        "commissionStatus": "pending",
        "commissionAmount": {"amount": 30, "currency": "GBP"},
        "saleAmount": {"amount": 1, "currency": "GBP"},
        "transactionDate": "2026-08-30T00:00:00",
        "validationDate": None,
        "orderRef": "mock-order-002",
    },
    {
        "id": 233982939,
        "advertiserId": ADVERTISER_ID,
        "publisherId": 231221,
        "siteName": "Example Publisher",
        "commissionStatus": "approved",
        "commissionAmount": {"amount": 12.5, "currency": "GBP"},
        "saleAmount": {"amount": 1, "currency": "GBP"},
        "transactionDate": "2026-08-30T12:00:00",
        "validationDate": "2026-08-30T13:00:00",
        "orderRef": "mock-order-003",
    },
]


@app.get("/advertisers/<int:advertiser_id>/transactions/")
def get_transactions(advertiser_id):
    date_type = request.args.get("dateType", "transaction")
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    timezone_name = request.args.get("timezone")

    if date_type not in {"transaction", "validation"}:
        return jsonify({"error": "dateType must be transaction or validation"}), 400, build_json_response_headers()
    if not start_date or not end_date or not timezone_name:
        return jsonify({"error": "startDate, endDate, and timezone are required"}), 400, build_json_response_headers()
    if advertiser_id != ADVERTISER_ID:
        return jsonify([]), 200, build_json_response_headers()

    try:
        start_value = datetime.fromisoformat(start_date)
        end_value = datetime.fromisoformat(end_date)
        page = max(1, int(request.args.get("page", 1)))
        page_size = max(1, int(request.args.get("pageSize", 10000)))
    except ValueError:
        return jsonify({"error": "invalid ISO dates or pagination values"}), 400, build_json_response_headers()

    date_field = "transactionDate" if date_type == "transaction" else "validationDate"
    matching_transactions = []
    for transaction in TRANSACTIONS:
        transaction_date = transaction.get(date_field)
        if transaction_date and start_value <= datetime.fromisoformat(transaction_date) <= end_value:
            matching_transactions.append(transaction)

    first = (page - 1) * page_size
    return jsonify(matching_transactions[first:first + page_size]), 200, build_json_response_headers()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
