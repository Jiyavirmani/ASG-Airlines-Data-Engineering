# ASG Airlines — Analytical Data Model

## 1. Purpose

The analytical layer converts cleaned operational data into business-ready tables that can be consumed by reporting and business intelligence tools.

The model is designed to support:

- Flight duration analysis
- Route-wise traffic analysis
- Airline performance analysis
- Booking trends
- Payment analysis
- Data quality and anomaly reporting

---

## 2. Data Flow

```text
                    RAW SOURCE

                        │

                        ▼

              ┌──────────────────┐
              │ Excel Workbook   │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Cleaning &       │
              │ Validation       │
              └────────┬─────────┘
                       │
              ┌────────┴─────────┐
              ▼                  ▼
       Valid / Cleaned       Quarantine
              │                  │
              ▼                  ▼
       GOLD ANALYTICAL       Invalid /
           LAYER             Anomalous Data
              │
              ▼
           Power BI
```

---

## 3. Analytical Tables

### 3.1 fact_flights

Contains validated flight-level operational data.

Important fields include:

- `flight_id`
- `airline`
- `source`
- `destination`
- `route`
- `departure_time`
- `arrival_time`
- `departure_date`
- `flight_duration_minutes`
- `overnight_flag`

This table is used for flight duration, route and airline analysis.

### 3.2 fact_bookings

Contains cleaned booking-level information.

Important fields include:

- `booking_id`
- `passenger_id`
- `flight_id`
- `status`
- `seat_number`
- `is_confirmed`
- `is_cancelled`
- `is_pending`
- `is_invalid`

This table supports booking-status and booking-volume analysis.

### 3.3 fact_payments

Contains valid payment transactions.

Important fields include:

- `payment_id`
- `booking_id`
- `payment_method`
- `payment_amount`

Invalid payment amounts are excluded from the valid payment analytical table and retained separately in quarantine.

### 3.4 route_summary

Contains aggregated route-level metrics:

- Total flights
- Average flight duration
- Median flight duration
- Overnight flights
- Overnight-flight percentage

### 3.5 airline_summary

Contains aggregated airline-level metrics:

- Total flights
- Average flight duration
- Median flight duration
- Overnight flights
- Flight share percentage

### 3.6 booking_summary

Contains aggregated booking-status metrics:

- Booking status
- Total bookings
- Percentage of bookings

### 3.7 payment_summary

Contains aggregated payment-method metrics:

- Total transactions
- Total payment amount
- Average payment amount

### 3.8 kpi_summary

Contains high-level business KPIs:

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

---

## 4. Logical Relationships

The operational datasets have the following logical relationships:

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

The analytical layer primarily uses the validated flight, booking and payment datasets.

Passenger PII is not required for the core business KPIs and should therefore not be unnecessarily exposed in reporting.

---

## 5. Business KPI Mapping

| Business Requirement | Analytical Table | Main Metric |
|---|---|---|
| Average Flight Duration | `fact_flights` / `kpi_summary` | Average duration |
| Route-wise Traffic | `route_summary` | Total flights by route |
| Delay / Anomaly Insights | `fact_flights` | Temporal and duration anomalies |
| Distribution by Airline | `airline_summary` | Flights by airline |
| Booking Analysis | `booking_summary` | Booking status distribution |
| Payment Analysis | `payment_summary` | Transactions and payment value |

---

## 6. Flight Duration Logic

Flight duration is calculated using the complete departure and arrival timestamps.

```text
Flight Duration
=
Arrival Timestamp
-
Departure Timestamp
```

This approach correctly handles flights that cross midnight.

For example:

```text
Departure: 20-Apr-2026 23:38
Arrival:   21-Apr-2026 02:32
```

The flight is treated as an overnight flight rather than incorrectly producing a negative duration.

---

## 7. Anomaly Handling

The pipeline identifies:

- Invalid timestamp records
- Arrival-before-departure records
- Duration mismatches
- Missing or unknown airline information
- Duplicate or conflicting flight records
- Invalid booking statuses
- Invalid payment amounts
- Referential-integrity issues

Unusable records are preserved separately in the quarantine layer.

---

## 8. Delay Analysis Limitation

The source data does not provide separate scheduled and actual flight timestamps.

Therefore, conventional delay calculations cannot be reliably performed.

The project instead reports supported operational anomalies such as:

- Invalid temporal sequences
- Duration inconsistencies
- Missing or unknown airline information
- Duplicate or conflicting flight records

This prevents unsupported delay metrics from being presented as factual results.

---

## 9. PII and Reporting

The passenger dataset contains personally identifiable information, including:

- Names
- Email addresses
- Phone numbers
- Aadhaar IDs
- Date of birth

These fields are not required for the core operational KPIs.

Therefore:

- Sensitive passenger information should not be displayed in Power BI dashboards.
- Access to raw PII should be restricted to authorized users.
- Analytical datasets should contain only information required for the business analysis.

---

## 10. Data Quality and Quarantine

The pipeline separates usable analytical records from records that cannot be safely used.

```text
Raw Data
    │
    ▼
Validation
    │
    ├───────────────┐
    ▼               ▼
Valid Records    Invalid /
    │            Anomalous Records
    ▼               │
Gold Layer          ▼
    │           Quarantine
    ▼
Power BI
```

Examples of quarantined records include:

- Flights with invalid temporal sequences
- Flights with invalid timestamps
- Payments with missing amounts
- Payments with unparseable amounts

Questionable but still usable records can remain in the cleaned dataset with appropriate quality flags.

---

## 11. KPI Definitions

### Total Flights

```text
Total Flights = Count of valid flight records
```

### Average Flight Duration

```text
Average Flight Duration
=
Sum of Valid Flight Durations
/
Number of Valid Flights
```

### Route-wise Traffic

```text
Route Traffic
=
Count of Valid Flights
grouped by Source and Destination
```

### Airline Flight Share

```text
Airline Flight Share (%)
=
Airline Flight Count
/
Total Valid Flights
× 100
```

### Overnight Flight Percentage

```text
Overnight Flight (%)
=
Overnight Flights
/
Total Valid Flights
× 100
```

### Confirmed Booking Rate

```text
Confirmed Booking Rate (%)
=
Confirmed Bookings
/
Total Bookings
× 100
```

### Cancellation Rate

```text
Cancellation Rate (%)
=
Cancelled Bookings
/
Total Bookings
× 100
```

### Pending Booking Rate

```text
Pending Booking Rate (%)
=
Pending Bookings
/
Total Bookings
× 100
```

### Total Payment Value

```text
Total Payment Value
=
Sum of Valid Payment Amounts
```

Invalid or unparseable payment amounts are excluded.

---

## 12. Data Quality Metrics

The project measures:

- Total records
- Missing values
- Duplicate records
- Invalid records
- Temporal anomalies
- Duration mismatches
- Invalid booking statuses
- Invalid payment amounts
- Referential-integrity violations
- Overnight flight count

---

## 13. Layered Architecture

The project follows:

```text
RAW
 ↓
PROCESSED
 ↓
VALID / QUARANTINE
 ↓
GOLD
 ↓
POWER BI
```

Each layer has a specific responsibility:

- **Raw:** preserve original source data
- **Processed:** clean and validate data
- **Quarantine:** isolate unusable records
- **Gold:** create business-ready analytical tables
- **Power BI:** visualize business KPIs and insights

---

## 14. Design Principles

The analytical model follows these principles:

1. Preserve raw source data.
2. Separate cleaning from analytical processing.
3. Do not silently discard problematic records.
4. Quarantine records that cannot be safely resolved.
5. Use validated timestamps for duration calculations.
6. Correctly handle overnight flights.
7. Avoid unnecessary exposure of PII.
8. Calculate only KPIs supported by the available data.
9. Maintain traceability between source and analytical data.
10. Keep business rules documented and reproducible.
11. Use measurable data-quality metrics.
12. Design analytical outputs for downstream BI consumption.

---

## 15. Final Analytical Structure

```text
data/
│
├── raw/
│   └── UseCase - Airlines.xlsx
│
├── processed/
│   ├── flights_cleaned.csv
│   ├── flights_valid.csv
│   ├── bookings_cleaned.csv
│   ├── passengers_cleaned.csv
│   ├── payments_cleaned.csv
│   └── payments_valid.csv
│
├── quarantine/
│   ├── flights_quarantine.csv
│   └── payments_quarantine.csv
│
└── gold/
    ├── fact_flights.csv
    ├── fact_bookings.csv
    ├── fact_payments.csv
    ├── route_summary.csv
    ├── airline_summary.csv
    ├── booking_summary.csv
    ├── payment_summary.csv
    ├── kpi_summary.csv
    └── dashboard_metrics.csv
```

---

## 16. Conclusion

The analytical data model provides a structured path from raw airline operational data to business-ready reporting.

The layered approach ensures that:

- Source data remains preserved.
- Data-quality issues are identified.
- Unusable records are quarantined.
- Valid data is transformed into analytical tables.
- Business KPIs are calculated consistently.
- Sensitive passenger information is minimized in reporting.
- Power BI can consume structured analytical outputs.
- Transformation and business rules remain traceable and explainable.