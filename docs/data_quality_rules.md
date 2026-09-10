# ASG Airlines — Data Quality Rules

This document defines the data quality rules used for the ASG Airlines data engineering pipeline. The purpose is to make cleaning and validation decisions explicit, reproducible, and explainable.

Raw source data is preserved separately. Cleaning operations are applied to create reliable analytical datasets, while records that cannot be safely resolved are flagged or moved to quarantine rather than silently discarded.

---

## 1. Flight Data Rules

### 1.1 Exact Duplicate Rows

Exact duplicate rows are identified during data validation.

- Duplicate records are removed from the cleaned analytical dataset.
- The original records remain available in the raw dataset.
- The number of removed duplicate records is recorded in the data quality report.

### 1.2 Duplicate Flight IDs

A duplicate `flight_id` does not automatically mean that a record is invalid.

- Duplicate flight IDs are investigated using the other flight attributes.
- Records with the same flight ID but different operational attributes are treated as potential business-key conflicts.
- Such records are not blindly deleted.
- Conflicting records are flagged for review.

### 1.3 Missing Airline Values

Missing airline values are not inferred from the flight ID or other fields without a defined business rule.

- Missing airline values are standardized to `UNKNOWN`.
- A data quality flag is created to identify records where the airline was originally missing.

### 1.4 Existing UNKNOWN Airline Values

Existing `UNKNOWN` airline values are retained.

- They are treated as valid categorical values for storage.
- They are flagged as incomplete airline information.
- They are included in data quality reporting.

### 1.5 Timestamp Standardization

`departure_time` and `arrival_time` are converted into a standardized datetime format.

- Valid datetime values are parsed consistently.
- Unparseable timestamp values are considered invalid.
- Invalid timestamp records are flagged and excluded from reliable duration calculations.

### 1.6 Flight Duration

Flight duration is recalculated using the standardized departure and arrival timestamps.

The analytical duration is calculated as:

`arrival_time - departure_time`

The source `duration` field is treated as a source value and can be compared against the recalculated duration for validation.

### 1.7 Overnight Flights

Flights crossing midnight are considered valid when the arrival timestamp occurs on the following calendar day.

For example:

- Departure: `2026-04-20 23:38:41`
- Arrival: `2026-04-21 02:32:41`

The full timestamps are used when calculating duration so that overnight flights are not incorrectly treated as negative or unusually short flights.

### 1.8 Invalid Temporal Sequence

A flight is flagged as a temporal anomaly when the arrival timestamp occurs before the departure timestamp and cannot be resolved using a valid overnight interpretation.

Such records:

- remain available in the raw data;
- are flagged as temporal anomalies;
- are not used for reliable flight-duration analytics unless a valid correction rule can be justified.

---

## 2. Booking Data Rules

### 2.1 Blank Records

Completely blank booking rows are treated as invalid/incomplete records.

They are removed from the cleaned analytical dataset while the raw source remains preserved.

### 2.2 Duplicate Booking Records

Exact duplicate booking rows are identified during validation.

- Exact duplicates are removed from the cleaned dataset.
- The duplicate count is recorded in the data quality report.

### 2.3 Booking Status

Booking status values are standardized using the values present in the source data.

Expected statuses include:

- `CONFIRMED`
- `CANCELLED`
- `PENDING`
- `INVALID`

Missing or invalid status values are retained but flagged for data quality analysis.

### 2.4 Booking-to-Passenger Relationship

Each valid booking should reference an existing passenger through `passenger_id`.

Records with missing or unmatched passenger references are flagged as referential-integrity issues.

### 2.5 Booking-to-Flight Relationship

Each valid booking should reference an existing flight through `flight_id`.

Records with missing or unmatched flight references are flagged as referential-integrity issues.

---

## 3. Passenger Data Rules

The passenger dataset contains personally identifiable information (PII).

PII fields include information such as:

- passenger names
- email addresses
- phone numbers
- Aadhaar IDs
- dates of birth

### 3.1 Passenger IDs

`passenger_id` is treated as the primary identifier for passenger records.

Duplicate or conflicting passenger identifiers are investigated before inclusion in the analytical layer.

### 3.2 Missing Passenger Attributes

Missing passenger attributes are retained where appropriate and flagged rather than being replaced with arbitrary values.

No demographic value should be guessed from other fields.

### 3.3 PII Protection

PII should not be unnecessarily exposed in analytical or reporting datasets.

The Power BI/reporting layer should use only the passenger information required for business analysis.

Sensitive fields such as Aadhaar numbers, phone numbers, and personal email addresses should not be exposed in dashboard visuals.

---

## 4. Payment Data Rules

### 4.1 Payment IDs

`payment_id` should uniquely identify a payment record.

Duplicate payment IDs are investigated as potential data quality issues.

### 4.2 Payment Amount

Payment amounts should be numeric and greater than zero when present.

Missing payment amounts are flagged.

Non-positive payment amounts are treated as potential anomalies and excluded from financial aggregation unless a justified business rule exists.

### 4.3 Payment Methods

Payment methods are standardized using the values present in the source data.

Expected payment methods include:

- `CARD`
- `UPI`
- `NETBANKING`

Unexpected values are flagged.

### 4.4 Payment-to-Booking Relationship

Each payment should reference a valid `booking_id`.

Unmatched booking references are flagged as referential-integrity issues.

Multiple payment records for the same booking are not automatically considered duplicates because the available data does not establish whether they represent retries, partial payments, refunds, or other legitimate transactions.

---

## 5. Referential Integrity Rules

Relationships between the datasets are validated before creating the analytical model.

The main relationships are:

```text
Bookings → Passengers
Bookings → Flights
Payments → Bookings
