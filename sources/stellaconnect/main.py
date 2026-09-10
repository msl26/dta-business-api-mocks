"""Generic mock StellaConnect Surveys API for development and testing."""

from datetime import datetime, timedelta, timezone
import json

from flask import Flask, jsonify, request

from shared.response_headers import build_json_response_headers

app = Flask(__name__)

ROW_SIZE_LIMIT_BYTES = 2 * 1024 * 1024


def build_record(sequence_id, created_at, completed_at, scenario, response_headers):
    record = {
        "uuid": f"mock-survey-{sequence_id}",
        "sequence_id": sequence_id,
        "branding": "mock",
        "channel": "web",
        "ext_interaction_id": f"MOCK_{sequence_id}",
        "language": "en",
        "survey_id": 501,
        "survey_name": "Mock Survey",
        "tags": ["mock"],
        "request_created_at": created_at,
        "response_received_at": completed_at,
        "employee": {"custom_id": f"EMP_{sequence_id}"},
        "customer": {"full_name": f"Mock Customer {sequence_id}"},
        "scenario": scenario,
        "row_payload": "",
    }
    line_data = {"response_headers": response_headers, "record": record}
    base_size = len(json.dumps(line_data, separators=(",", ":")).encode("utf-8")) + 1
    record["row_payload"] = "A" * max(ROW_SIZE_LIMIT_BYTES - 65536 - base_size, 0)
    return record


def mock_records(response_headers):
    yesterday = datetime.now(timezone.utc).date() - timedelta(days=1)
    yesterday_text = yesterday.isoformat()
    return [
        build_record(
            301,
            "2023-01-15T10:00:00.000Z",
            "2023-01-15T11:00:00.000Z",
            "historical",
            response_headers,
        ),
        build_record(
            302,
            f"{yesterday_text}T10:00:00.000Z",
            f"{yesterday_text}T11:00:00.000Z",
            "recent",
            response_headers,
        ),
    ]


def parse_datetime(value, upper_bound=False):
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if len(value) == 10 and upper_bound:
        parsed = parsed.replace(hour=23, minute=59, second=59)
    if parsed.tzinfo is not None:
        parsed = parsed.replace(tzinfo=None)
    return parsed


def in_range(record_value, lower_value, upper_value):
    record_time = parse_datetime(record_value)
    lower_time = parse_datetime(lower_value)
    upper_time = parse_datetime(upper_value, upper_bound=True)
    return bool(record_time and lower_time and upper_time and lower_time <= record_time <= upper_time)


@app.get("/surveys")
def get_surveys():
    created_at_gte = request.args.get("created_at_gte")
    created_at_lte = request.args.get("created_at_lte")
    completed_at_gte = request.args.get("completed_at_gte")
    completed_at_lte = request.args.get("completed_at_lte")
    response_headers = build_json_response_headers(include_security_headers=True)
    records = mock_records(response_headers)

    if completed_at_gte and completed_at_lte:
        records = [
            record for record in records
            if in_range(record["response_received_at"], completed_at_gte, completed_at_lte)
        ]
        if created_at_gte and created_at_lte:
            records = [
                record for record in records
                if in_range(record["request_created_at"], created_at_gte, created_at_lte)
            ]
        return jsonify(records), 200, response_headers

    if created_at_gte and created_at_lte:
        records = [
            record for record in records
            if in_range(record["request_created_at"], created_at_gte, created_at_lte)
        ]
        return jsonify(records), 200, response_headers

    return jsonify([]), 200, response_headers


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
