# DTA Business API Mocks

Development and test mock services for business API acquirers. These services
must not be deployed to production or used as production data sources.

## Repository layout

```text
shared/                     Common mock response helpers
sources/awin/               Awin Transactions API mock
sources/stellaconnect/      StellaConnect Surveys API mock
cloudbuild-awin.yaml        Independent Awin image build
cloudbuild-stellaconnect.yaml Independent StellaConnect image build
```

Each source builds and deploys as a separate Cloud Run service. Adding a new
API means adding `sources/<api>/`, its Dockerfile, tests, and a separate Cloud
Build file.

## Local setup and tests

From the repository root:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s sources -p "test_app.py" -v
```

Run an individual service locally:

```powershell
python -m sources.awin.main
python -m sources.stellaconnect.main
```

## Build in dev or test

The build configurations reject project IDs that do not end in `-dev` or
`-test`.

```powershell
gcloud builds submit --config=cloudbuild-awin.yaml --project=<dev-or-test-project>
gcloud builds submit --config=cloudbuild-stellaconnect.yaml --project=<dev-or-test-project>
```

Deploy the resulting images as separate `mock-awin-api` and
`mock-stellaconnect-api` Cloud Run services. Configure dev/test acquirers with
the corresponding HTTPS service URL. Production acquirers must use the real
provider endpoints.

## Awin endpoint

```text
GET /advertisers/123456/transactions/
```

Required query parameters are `startDate`, `endDate`, and `timezone`. The mock
also supports `dateType`, `page`, and `pageSize`, and requires a Bearer header.

## StellaConnect endpoints

```text
GET /surveys
```

The surveys endpoint supports created and completed date-range filters and
returns generic historical and recent mock survey records.