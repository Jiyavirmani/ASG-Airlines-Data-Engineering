# ASG Airlines — Power BI Dashboard Design

## 1. Dashboard Objective

The Power BI dashboard provides an interactive view of airline operations using the validated analytical datasets created by the data pipeline.

The dashboard focuses on:

- Flight volume
- Flight duration
- Route traffic
- Airline distribution
- Booking status
- Payment activity
- Overnight flights
- Data-quality and anomaly insights

---

## 2. Dashboard Pages

The dashboard is organized into four primary pages:

1. Overview
2. Duration Analysis
3. Route Performance
4. Airline & Booking Trends

A dedicated anomaly and data-quality section is included where appropriate.

---

## 3. Page 1 — Overview

### Purpose

Provide a high-level summary of the airline dataset and the major operational KPIs.

### KPI Cards

The following KPI cards should be displayed:

- Total Flights
- Total Bookings
- Average Flight Duration
- Overnight Flights
- Valid Payment Transactions
- Total Payment Value

### Recommended Visuals

#### Flight Distribution by Airline

**Visual:** Bar chart

- Axis: Airline
- Value: Flight Count

Purpose:

Shows how flight volume is distributed across airlines.

#### Booking Status Distribution

**Visual:** Donut chart

- Legend: Booking Status
- Value: Booking Count

Purpose:

Shows the distribution of confirmed, cancelled, pending and invalid bookings.

#### Flight Route Volume

**Visual:** Bar chart

- Axis: Route
- Value: Total Flights

Purpose:

Highlights the busiest routes.

### Filters / Slicers

Recommended slicers:

- Airline
- Source
- Destination
- Departure Date

---

## 4. Page 2 — Duration Analysis

### Purpose

Analyze flight duration patterns and identify operational duration characteristics.

### KPI Cards

- Average Flight Duration
- Median Flight Duration
- Minimum Flight Duration
- Maximum Flight Duration
- Overnight Flight Percentage

### Recommended Visuals

#### Flight Duration Distribution

**Visual:** Histogram

- Axis: Flight Duration (Minutes)
- Value: Flight Count

Purpose:

Shows the distribution of flight durations.

#### Average Duration by Airline

**Visual:** Column chart

- Axis: Airline
- Value: Average Flight Duration

Purpose:

Compares average operational flight duration across airlines.

#### Overnight Flights

**Visual:** Column chart

- Axis: Airline
- Value: Overnight Flight Count

Purpose:

Shows which airlines operate more overnight flights.

### Filters

- Airline
- Source
- Destination
- Departure Date

---

## 5. Page 3 — Route Performance

### Purpose

Analyze traffic and duration patterns across flight routes.

### KPI Cards

- Total Routes
- Total Flights
- Average Flight Duration
- Overnight Flights

### Recommended Visuals

#### Top Routes by Flight Volume

**Visual:** Bar chart

- Axis: Route
- Value: Total Flights

Purpose:

Identifies the highest-volume routes.

#### Average Duration by Route

**Visual:** Bar chart

- Axis: Route
- Value: Average Flight Duration

Purpose:

Compares operational duration across routes.

#### Route Traffic Table

**Visual:** Table

Columns:

- Route
- Total Flights
- Average Flight Duration
- Median Flight Duration
- Overnight Flights
- Overnight Percentage

Purpose:

Provides detailed route-level analysis.

### Filters

- Source
- Destination
- Airline

---

## 6. Page 4 — Airline & Booking Trends

### Purpose

Analyze airline-level distribution and booking behavior.

### KPI Cards

- Total Flights
- Total Bookings
- Confirmed Booking Rate
- Cancellation Rate
- Pending Booking Rate

### Recommended Visuals

#### Flights by Airline

**Visual:** Bar chart

- Axis: Airline
- Value: Flight Count

#### Booking Status by Airline

**Visual:** Stacked column chart

- Axis: Airline
- Legend: Booking Status
- Value: Booking Count

Purpose:

Shows booking-status distribution across airlines.

#### Payment Method Distribution

**Visual:** Donut chart

- Legend: Payment Method
- Value: Transaction Count

#### Payment Value by Payment Method

**Visual:** Column chart

- Axis: Payment Method
- Value: Total Payment Amount

### Filters

- Airline
- Booking Status
- Payment Method

---

## 7. Data Quality and Anomaly Insights

The dashboard should provide visibility into important data-quality issues identified during the pipeline.

Recommended metrics:

- Missing Airline Records
- Unknown Airline Records
- Temporal Anomalies
- Invalid Booking Statuses
- Invalid Payment Amounts
- Referential-Integrity Violations

### Important Limitation

The source data does not contain separate scheduled and actual timestamps.

Therefore, conventional delay minutes cannot be calculated reliably.

The dashboard should report operational anomalies rather than presenting unsupported delay values.

---

## 8. Data Sources for Power BI

The primary Power BI sources are the Gold-layer datasets:

```text
data/gold/
│
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

Power BI should primarily consume the Gold-layer outputs rather than the raw Excel workbook.

---

## 9. Reporting Design Principles

The dashboard should follow these principles:

1. Keep KPI cards at the top of each page.
2. Use consistent naming for metrics.
3. Avoid unnecessary visual clutter.
4. Use slicers consistently across related pages.
5. Prefer business-readable labels over technical column names.
6. Do not expose passenger PII.
7. Clearly distinguish operational anomalies from conventional delays.
8. Use validated analytical data for reporting.
9. Keep visuals focused on actionable business insights.
10. Ensure every visual has a clear analytical purpose.

---

## 10. Expected Business Questions

The dashboard should help answer questions such as:

- How many valid flights are present?
- What is the average flight duration?
- Which routes have the highest traffic?
- Which airlines operate the most flights?
- What percentage of flights are overnight?
- What is the distribution of booking statuses?
- Which payment methods are most frequently used?
- Which routes have longer average durations?
- Where are the major data-quality issues?
- What operational anomalies were identified?

---

## 11. Dashboard Navigation

Recommended navigation:

```text
                    ASG AIRLINES
                         │
                         ▼
                    OVERVIEW
                   /    |    \
                  /     |     \
                 ▼      ▼      ▼
          DURATION   ROUTE   AIRLINE &
          ANALYSIS  PERFORMANCE  BOOKING
```

Each page should contain a consistent navigation mechanism so users can move between analytical views easily.

---

## 12. Privacy Considerations

Passenger-level personally identifiable information should not be included in dashboard visuals.

The dashboard should use aggregated operational and business metrics.

Sensitive fields such as:

- Passenger name
- Email
- Phone number
- Aadhaar ID
- Date of birth

should remain outside the reporting layer unless specifically required and authorized.

---

## 13. Final Dashboard Structure

```text
Power BI
│
├── Page 1 — Overview
│   ├── KPI Cards
│   ├── Flights by Airline
│   ├── Booking Status
│   └── Route Volume
│
├── Page 2 — Duration Analysis
│   ├── Duration KPIs
│   ├── Duration Distribution
│   ├── Duration by Airline
│   └── Overnight Flights
│
├── Page 3 — Route Performance
│   ├── Route KPIs
│   ├── Top Routes
│   ├── Average Duration by Route
│   └── Route Detail Table
│
└── Page 4 — Airline & Booking Trends
    ├── Booking KPIs
    ├── Flights by Airline
    ├── Booking Status by Airline
    ├── Payment Method Distribution
    └── Payment Value by Method
```

---

## 14. Conclusion

The Power BI dashboard is designed as the final reporting layer of the ASG Airlines data pipeline.

It transforms the Gold-layer analytical outputs into interactive business insights while maintaining data-quality, privacy and analytical limitations established during the earlier pipeline stages.