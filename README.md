# ASG Airlines — End-to-End Data Engineering Pipeline

## 1. Project Overview

This project implements an end-to-end data engineering pipeline for airline operational data.

The source workbook contains flight, booking, passenger and payment datasets with intentional data-quality issues such as:

- Duplicate records
- Missing values
- Unknown airline values
- Invalid payment amounts
- Invalid booking statuses
- Temporal anomalies
- Overnight flights
- Referential-integrity checks

The objective is to transform the raw source data into validated, business-ready analytical datasets that can support reporting and business intelligence.

---

## 2. Business Objectives

The pipeline supports analysis of:

- Average flight duration
- Route-wise traffic
- Airline flight distribution
- Booking status
- Payment activity
- Overnight flights
- Data-quality issues
- Operational anomalies

The project also provides structured Gold-layer datasets for downstream Power BI reporting.

---

## 3. Architecture

```text
                     RAW SOURCE
                         │
                         ▼
              ┌────────────────────┐
              │ Excel Workbook     │
              │ Flights             │
              │ Bookings            │
              │ Passengers          │
              │ Payments            │
              └──────────┬─────────┘
                         │
                         ▼
              ┌────────────────────┐
              │ Cleaning &         │
              │ Validation         │
              └──────────┬─────────┘
                         │
                 ┌───────┴────────┐
                 ▼                ▼
          Valid / Cleaned     Quarantine
                 │                │
                 ▼                ▼
          GOLD ANALYTICAL     Invalid /
              LAYER           Anomalous Data
                 │
                 ▼
          Dashboard Metrics
                 │
                 ▼
              Power BI
```

---

## 4. Data Layers

### Raw Layer

Contains the original Excel workbook.

```text
data/raw/
└── UseCase - Airlines.xlsx
```

The raw source is preserved and is not overwritten by downstream transformations.

### Processed Layer

Contains cleaned datasets and validated records.

```text
data/processed/
```

Examples include:

- `flights_cleaned.csv`
- `flights_valid.csv`
- `bookings_cleaned.csv`
- `passengers_cleaned.csv`
- `payments_cleaned.csv`
- `payments_valid.csv`

### Quarantine Layer

Contains records that cannot safely participate in the analytical layer.

```text
data/quarantine/
├── flights_quarantine.csv
└── payments_quarantine.csv
```

### Gold Layer

Contains business-ready analytical datasets.

```text
data/gold/
```

---

## 5. Data Quality Handling

The pipeline performs validation across the major datasets.

### Flights

The pipeline checks:

- Missing airline values
- Unknown airline values
- Invalid timestamps
- Arrival-before-departure anomalies
- Overnight flights
- Duration consistency

### Bookings

The pipeline checks:

- Booking status validity
- Passenger references
- Flight references

### Passengers

The pipeline checks:

- Date-of-birth validity
- Passenger-level data quality

### Payments

The pipeline checks:

- Missing payment amounts
- Unparseable payment amounts
- Non-positive payment amounts
- Booking references

---

## 6. Current Data Quality Results

The validated pipeline produced the following results:

| Metric | Result |
|---|---:|
| Valid flights | 1004 |
| Flight records quarantined | 1 |
| Valid payment transactions | 922 |
| Payment records quarantined | 78 |
| Invalid booking statuses | 45 |
| Missing airline records | 39 |
| Unknown airline records | 69 |
| Temporal flight anomalies | 1 |
| Overnight flights | 123 |
| Orphan passenger references | 0 |
| Orphan flight references | 0 |
| Orphan booking references | 0 |

The payment validation identified:

```text
48 missing payment amounts
+
30 unparseable "INVALID" payment amounts
=
78 invalid payment records
```

The invalid payment records are retained in quarantine rather than silently discarded.

---

## 7. Flight Duration Handling

Flight duration is calculated using complete departure and arrival timestamps.

```text
Flight Duration
=
Arrival Timestamp
-
Departure Timestamp
```

This allows flights crossing midnight to be handled correctly.

Example:

```text
Departure: 20-Apr-2026 23:38
Arrival:   21-Apr-2026 02:32
```

The flight is therefore treated as an overnight flight instead of producing an incorrect negative duration.

---

## 8. Anomaly Handling

The pipeline distinguishes between valid analytical records and records that cannot safely be used.

Examples include:

- Arrival before departure
- Invalid timestamps
- Invalid payment amounts
- Invalid booking statuses
- Data-quality inconsistencies

Records that cannot safely participate in the analytical layer are preserved in quarantine files.

---

## 9. Delay Analysis Limitation

The source dataset does not provide separate scheduled and actual flight timestamps.

Therefore, conventional delay minutes cannot be calculated reliably from the available data.

Instead, the project reports supported operational anomalies such as:

- Invalid temporal sequences
- Duration inconsistencies
- Data-quality issues

This avoids presenting unsupported delay calculations as factual business metrics.

---

## 10. Gold Analytical Layer

The Gold layer contains:

### Flight Fact

`fact_flights.csv`

Used for:

- Flight volume
- Flight duration
- Route analysis
- Airline analysis
- Overnight analysis

### Booking Fact

`fact_bookings.csv`

Used for:

- Booking volume
- Booking-status analysis
- Booking-quality analysis

### Payment Fact

`fact_payments.csv`

Used for:

- Valid payment transactions
- Payment method analysis
- Payment value analysis

### Aggregated Tables

```text
route_summary.csv
airline_summary.csv
booking_summary.csv
payment_summary.csv
kpi_summary.csv
dashboard_metrics.csv
```

---

## 11. Business KPIs

The project calculates:

- Total Flights
- Total Bookings
- Valid Payment Transactions
- Average Flight Duration
- Median Flight Duration
- Overnight Flights
- Confirmed Booking Rate
- Cancellation Rate
- Pending Booking Rate
- Total Payment Value

Additional analytical metrics are available through `dashboard_metrics.csv`.

---

## 12. Dashboard Metrics

The dashboard metrics layer combines business KPIs, data-quality metrics and additional analytical KPIs.

The generated dataset currently contains:

```text
33 metrics
```

Categories:

```text
Business KPI      10
Data Quality      16
Analytical KPI     7
```

This dataset is designed as a convenient reporting source for Power BI.

---

## 13. Data Model

The logical relationships are:

```text
Passengers
    │
    │ passenger_id
    ▼
Bookings
    │
    │ flight_id
    ▼
Flights

Bookings
    │
    │ booking_id
    ▼
Payments
```

Passenger-level personally identifiable information is not required for the core business KPIs and is therefore not exposed in the analytical reporting layer.

---

## 14. Privacy Considerations

The passenger dataset contains personally identifiable information including:

- Name
- Email
- Phone number
- Aadhaar ID
- Date of birth

These fields are not required for the operational KPIs.

Therefore:

- PII is excluded from the core dashboard layer.
- Raw passenger information should be restricted to authorized users.
- Reporting should use aggregated operational metrics wherever possible.

---

## 15. Project Structure

```text
ASG-Airlines-Data-Engineering/
│
├── data/
│   ├── raw/
│   │   └── UseCase - Airlines.xlsx
│   │
│   ├── processed/
│   │   ├── flights_cleaned.csv
│   │   ├── flights_valid.csv
│   │   ├── bookings_cleaned.csv
│   │   ├── passengers_cleaned.csv
│   │   ├── payments_cleaned.csv
│   │   └── payments_valid.csv
│   │
│   ├── quarantine/
│   │   ├── flights_quarantine.csv
│   │   └── payments_quarantine.csv
│   │
│   └── gold/
│       ├── fact_flights.csv
│       ├── fact_bookings.csv
│       ├── fact_payments.csv
│       ├── route_summary.csv
│       ├── airline_summary.csv
│       ├── booking_summary.csv
│       ├── payment_summary.csv
│       ├── kpi_summary.csv
│       └── dashboard_metrics.csv
│
├── docs/
│   ├── data_quality_rules.md
│   ├── data_quality_report.csv
│   ├── data_model.md
│   └── power_bi_dashboard.md
│
├── notebooks/
│   └── 01_data_profiling.ipynb
│
├── src/
│   ├── clean_data.py
│   ├── data_quality_report.py
│   ├── quarantine_records.py
│   ├── verify_quality.py
│   ├── create_gold_layer.py
│   ├── create_dashboard_metrics.py
│   └── run_pipeline.py
│
└── tests/
    └── test_pipeline.py
```

---

## 16. How to Run the Pipeline

### Environment

The project uses Python and pandas for the local implementation.

Activate the Conda environment:

```bash
conda activate asg-airlines
```

### Run the Complete Pipeline

The entire pipeline can be executed with one command:

```bash
python src/run_pipeline.py
```

The pipeline executes:

```text
Cleaning
   ↓
Data Quality Report
   ↓
Quarantine
   ↓
Quality Verification
   ↓
Gold Layer
   ↓
Dashboard Metrics
```

---

## 17. Automated Testing

The project uses `pytest` for automated validation.

Run:

```bash
python -m pytest tests/test_pipeline.py -v
```

Current test coverage includes:

- Valid flight count
- Flight quarantine count
- Valid payment count
- Payment quarantine count
- Passenger referential integrity
- Flight referential integrity
- Payment referential integrity
- Gold-table existence
- Gold flight count
- Gold payment count
- Dashboard metric count

Current validation result:

```text
11 passed
```

---

## 18. Power BI Reporting

The Gold-layer datasets are designed for downstream Power BI reporting.

The planned dashboard contains:

### Page 1 — Overview

- Total Flights
- Total Bookings
- Average Flight Duration
- Overnight Flights
- Payment metrics
- Flight distribution by airline
- Booking status distribution

### Page 2 — Duration Analysis

- Average duration
- Median duration
- Duration distribution
- Duration by airline
- Overnight flight analysis

### Page 3 — Route Performance

- Route traffic
- Average duration by route
- Route-level analytical table
- Overnight route analysis

### Page 4 — Airline & Booking Trends

- Flights by airline
- Booking status by airline
- Payment method distribution
- Payment value by payment method

Conventional delay minutes are not displayed because the source data does not contain the required scheduled-versus-actual timestamps.

---

## 19. Key Analytical Insights

The current pipeline establishes several measurable observations:

- 1004 flight records are available for the validated analytical layer.
- One flight record was quarantined because of a temporal anomaly.
- 922 payment transactions contain valid numeric amounts.
- 78 payment records require exclusion from payment-value analysis.
- 123 flights cross midnight in the source data.
- 45 booking records have invalid or missing booking statuses.
- Referential-integrity checks found no orphan passenger or payment references.
- The booking-to-flight relationship remains traceable even when a referenced flight is quarantined.

These observations are derived from the actual processed dataset rather than assumed business values.

---

## 20. Scalability and Engineering Considerations

The current implementation uses local Python and pandas because the assignment permits a local implementation as an alternative to cloud-based Azure services.

For larger production-scale datasets, the same architecture could be migrated to technologies such as:

- Azure Data Factory
- Azure Databricks
- Apache Spark
- Microsoft Fabric
- Cloud object storage
- SQL-based analytical warehouses

The logical separation between raw, processed, quarantine and Gold layers is designed to support such migration.

---

## 21. Design Principles

The project follows these principles:

1. Preserve raw source data.
2. Separate cleaning from analytical processing.
3. Validate data before analytical use.
4. Do not silently discard invalid records.
5. Quarantine unusable records.
6. Correctly handle overnight flights.
7. Maintain referential integrity.
8. Minimize exposure of PII.
9. Calculate only metrics supported by the source data.
10. Keep transformations reproducible.
11. Maintain measurable data-quality checks.
12. Provide automated validation through tests.

---

## 22. Limitations

The project has several source-data limitations:

- Scheduled and actual timestamps are not separately available.
- Conventional delay minutes cannot therefore be calculated.
- Airline values contain missing and unknown entries.
- Payment records contain missing and unparseable amounts.
- Passenger PII exists in the source dataset but is not required for operational reporting.
- Multiple payment transactions may exist for a booking; therefore payment totals should not automatically be interpreted as recognized revenue without additional payment-status information.

These limitations are explicitly documented rather than hidden during transformation.

---

## 23. Conclusion

The ASG Airlines pipeline transforms a deliberately imperfect airline dataset into a validated analytical structure suitable for business reporting.

The solution provides:

- Reproducible data ingestion
- Cleaning and validation
- Data-quality reporting
- Quarantine handling
- Referential-integrity checks
- Overnight-flight duration handling
- Gold-layer analytical tables
- Dashboard-ready metrics
- Automated tests
- Documented business rules
- PII-aware reporting design

The result is a traceable end-to-end data engineering workflow from raw source data to business-ready analytics.