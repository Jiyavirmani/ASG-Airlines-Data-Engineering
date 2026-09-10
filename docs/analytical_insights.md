# Analytical Insights

## 1. Purpose

This document summarizes quantitative insights derived from the cleaned and aggregated Gold-layer data produced by the ASG Airlines data engineering pipeline.

The analysis focuses on:

- Flight duration patterns
- Overnight flight behavior
- Airline distribution
- Booking status distribution
- Route-level traffic and duration
- Payment data quality
- Data quality and anomaly indicators

All values in this document are derived from the project's processed Gold-layer outputs.

---

## 2. Flight Duration Analysis

### 2.1 Average and Median Duration

The Gold-layer KPI table reports:

| Metric | Value |
|---|---:|
| Total valid flights | 1,004 |
| Average flight duration | 164.49 minutes |
| Median flight duration | 166 minutes |

The average duration is approximately:

**164.49 minutes = 2 hours 44 minutes**

The median duration is:

**166 minutes = 2 hours 46 minutes**

### Formula

Average flight duration:

\[
\text{Average Duration} =
\frac{\sum \text{Flight Duration}}{\text{Number of Valid Flights}}
\]

For this dataset:

\[
\text{Average Duration} \approx 164.49 \text{ minutes}
\]

### Interpretation

The mean and median are relatively close:

\[
166 - 164.49 = 1.51 \text{ minutes}
\]

This small difference suggests that the overall flight-duration distribution is not being strongly shifted by a small number of extremely long or short flights.

The median is useful alongside the mean because it represents the middle observation and is less sensitive to extreme values.

---

## 3. Overnight Flight Analysis

The Gold-layer KPI table reports:

- Total valid flights: **1,004**
- Overnight flights: **122**

The percentage of valid flights classified as overnight is:

\[
\text{Overnight Percentage}
=
\frac{122}{1004}\times100
\]

\[
\approx 12.15\%
\]

Therefore, approximately **12.15% of valid flights are overnight/cross-day flights**.

### Interpretation

Overnight flights are important for duration calculations because the arrival timestamp can occur on the following calendar day.

For example:

```text
Departure: 23:38
Arrival:   02:32 (next day)
```

The pipeline calculates duration using the timestamp difference rather than assuming that arrival must occur on the same calendar date.

This prevents valid overnight flights from being incorrectly classified as negative-duration flights.

---

## 4. Airline Distribution

The Gold-layer airline summary contains the following flight distribution:

| Airline | Flights | Flight Share |
|---|---:|---:|
| IndiGo | 249 | 24.80% |
| SpiceJet | 235 | 23.41% |
| Air India | 233 | 23.21% |
| Vistara | 218 | 21.71% |
| UNKNOWN | 69 | 6.87% |

### Formula

Airline flight share:

\[
\text{Flight Share (\%)} =
\frac{\text{Airline Flights}}
{\text{Total Valid Flights}}
\times100
\]

For IndiGo:

\[
\frac{249}{1004}\times100
\approx24.80\%
\]

### Interpretation

The four identified airlines have relatively similar flight volumes.

IndiGo has the largest share at approximately **24.80%**, while Vistara has the smallest identified-airline share at approximately **21.71%**.

The dataset also contains **69 flights classified as UNKNOWN**, representing approximately **6.87%** of valid flights.

This highlights the importance of retaining data-quality indicators rather than silently replacing missing or unknown airline values.

---

## 5. Booking Status Distribution

The Gold-layer KPI table reports:

| Booking Status | Count | Rate |
|---|---:|---:|
| CONFIRMED | 320 | 32.00% |
| CANCELLED | 314 | 31.40% |
| PENDING | 291 | 29.10% |

The remaining records represent statuses that are not included in these three KPI rates.

### Formula

Booking status rate:

\[
\text{Status Rate (\%)} =
\frac{\text{Bookings with Status}}
{\text{Total Bookings}}
\times100
\]

For confirmed bookings:

\[
\frac{320}{1000}\times100
=32.00\%
\]

For cancelled bookings:

\[
\frac{314}{1000}\times100
=31.40\%
\]

For pending bookings:

\[
\frac{291}{1000}\times100
=29.10\%
\]

### Interpretation

The booking dataset does not show a dominant status.

Confirmed bookings account for **32.00%**, while cancelled bookings account for **31.40%** and pending bookings for **29.10%**.

The relatively high cancellation and pending proportions indicate that booking status should be treated as an important operational dimension for dashboard analysis.

---

## 6. Route-Level Analysis

The `route_summary.csv` Gold-layer table provides route-level measures including:

- Total flights
- Average duration
- Median duration
- Overnight flights
- Overnight percentage

Example routes include:

| Route | Median Duration | Overnight Flights | Overnight % |
|---|---:|---:|---:|
| BLR → BOM | 140.5 min | 7 | 11.67% |
| BLR → CCU | 97 min | 4 | 19.05% |
| BLR → DEL | 125 min | 1 | 5.26% |
| BLR → HYD | 167 min | 3 | 15.79% |
| BLR → MAA | 219 min | 2 | 12.50% |

### Interpretation

Route-level aggregation allows operational characteristics to be compared without examining individual flight records.

For example, among the routes shown:

- **BLR → MAA** has the highest median duration at 219 minutes.
- **BLR → CCU** has the highest overnight percentage at 19.05%.
- **BLR → DEL** has the lowest overnight percentage at 5.26%.

These metrics can be used in Power BI to identify routes with different duration and overnight-flight characteristics.

---

## 7. Payment Data Analysis

The Gold-layer KPI table reports:

| Metric | Value |
|---|---:|
| Total payment records | 1,000 |
| Valid payment transactions | 922 |
| Total payment value | 7,385,143 |

The percentage of payment records retained as valid transactions is:

\[
\frac{922}{1000}\times100
=92.2\%
\]

Therefore:

**Valid payment transaction rate = 92.2%**

The remaining:

\[
1000-922=78
\]

payment records were quarantined because their payment amount was invalid.

### Important Interpretation

The value of **7,385,143** represents the sum of valid payment amounts in the processed payment dataset.

It should **not automatically be interpreted as airline revenue**, because the source data contains multiple payment records associated with some bookings and does not provide a payment-status field sufficient to distinguish successful payments, retries, refunds, or other transaction states.

Therefore, this metric is reported as:

> **Total Payment Value**

rather than:

> **Revenue**

This avoids overstating what the available data can support.

---

## 8. Data Quality Analysis

The pipeline identified several important data-quality conditions.

### Flights

- Total processed flight records: **1,005**
- Valid Gold-layer flights: **1,004**
- Quarantined flight records: **1**
- Missing airline values: **39**
- UNKNOWN airline values: **69**
- Temporal anomalies: **1**

The temporal anomaly was isolated rather than included in the valid analytical flight dataset.

### Payments

- Raw payment records: **1,000**
- Valid payment records: **922**
- Quarantined payment records: **78**
- Missing payment amounts: **48**
- Unparseable payment amounts: **30**
- Non-positive payment amounts: **0**

The payment invalid-record rate is:

\[
\frac{78}{1000}\times100
=7.8\%
\]

Therefore:

**7.8% of payment records required quarantine.**

The valid payment rate is:

\[
\frac{922}{1000}\times100
=92.2\%
\]

---

## 9. Data Quality Metrics

The pipeline uses explicit quality flags and quarantine outputs instead of silently deleting problematic records.

Examples include:

- `airline_missing_flag`
- `airline_unknown_flag`
- `invalid_timestamp_flag`
- `temporal_anomaly_flag`
- `overnight_flag`
- `duration_mismatch_flag`

This allows analytical datasets to remain clean while preserving visibility into the underlying data-quality problems.

### Quarantine principle

The processing logic follows:

```text
Raw Record
    |
    +-- Valid --------------------> Gold / Analytical Layer
    |
    +-- Invalid or Anomalous -----> Quarantine Layer
```

This provides traceability between source data and analytical outputs.

---

## 10. Flight Duration Calculation

The calculated flight duration is based on the difference between arrival and departure timestamps:

\[
\text{Duration Minutes}
=
\frac{\text{Arrival Timestamp} -
\text{Departure Timestamp}}
{60\text{ seconds}}
\]

For valid overnight flights, the timestamps naturally span two calendar dates.

This approach is preferable to calculating duration using only the time-of-day components because it correctly handles cross-day flights.

Where a source-provided duration exists, the pipeline also calculates:

\[
\text{Duration Difference}
=
\text{Calculated Duration}
-
\text{Source Duration}
\]

This provides a validation mechanism for identifying duration mismatches.

---

## 11. Delay Analysis Limitation

The source dataset does not contain the separate scheduled and actual departure/arrival timestamps required to calculate conventional airline delay metrics.

Therefore, the project does **not** claim to calculate:

- Average departure delay
- Average arrival delay
- On-time performance percentage
- Flights delayed by more than a specific number of minutes

Instead, the pipeline focuses on measurable temporal anomalies such as:

- Arrival occurring before departure
- Invalid timestamps
- Overnight/cross-day flights
- Duration inconsistencies

This keeps the analysis aligned with what the available source data can actually support.

---

## 12. Key Mathematical Observations

### 12.1 Mean-Median Difference

\[
\text{Mean-Median Difference}
=
164.49-166
=
-1.51\text{ minutes}
\]

The absolute difference is only:

\[
|\!-1.51|=1.51\text{ minutes}
\]

This indicates that the mean and median duration are close for the valid flight population.

---

### 12.2 Overnight Flight Rate

\[
\frac{122}{1004}\times100
\approx12.15\%
\]

Approximately **1 in every 8 valid flights** is classified as overnight/cross-day.

---

### 12.3 Payment Data Retention

\[
\frac{922}{1000}\times100
=92.2\%
\]

The pipeline successfully retained **92.2%** of payment records as valid analytical transactions.

---

### 12.4 Payment Quarantine Rate

\[
\frac{78}{1000}\times100
=7.8\%
\]

Therefore, **7.8%** of payment records require data-quality remediation before being considered valid transactions.

---

### 12.5 Airline Concentration

The four identified airlines account for:

\[
100\%-6.87\%=93.13\%
\]

of valid flights.

Therefore, approximately **93.13%** of valid flights have an identified airline value, while **6.87%** are classified as UNKNOWN.

---

## 13. Business Implications

The quantitative analysis supports several operational observations:

1. **Flight duration is relatively stable at the aggregate level**, with an average of 164.49 minutes and a median of 166 minutes.

2. **Overnight flights represent a meaningful operational category**, accounting for approximately 12.15% of valid flights.

3. **Airline traffic is relatively balanced** among the four identified airlines, with each contributing approximately 21.71%–24.80% of valid flights.

4. **Booking statuses are distributed across confirmed, cancelled, and pending states**, making booking-status analysis useful for operational reporting.

5. **Payment data requires quality controls**, with 7.8% of payment records quarantined.

6. **Data-quality transparency is important**, particularly for missing/unknown airline information and invalid payment values.

7. **Traditional delay analysis cannot be performed reliably** without scheduled-versus-actual timestamp fields.

---

## 14. Dashboard Applications

These measurements can directly support the Power BI dashboard.

### Overview

Recommended KPI cards:

- Total Flights: **1,004**
- Total Bookings: **1,000**
- Average Flight Duration: **164.49 min**
- Overnight Flights: **122**
- Valid Payment Transactions: **922**

### Duration Analysis

Recommended visuals:

- Average duration by airline
- Median duration by airline
- Average duration by route
- Overnight percentage by route

### Route Performance

Recommended visuals:

- Flights by route
- Average duration by route
- Median duration by route
- Overnight flights by route

### Airline & Booking Trends

Recommended visuals:

- Flight share by airline
- Flights by airline
- Booking status distribution
- Booking rate KPIs

### Data Quality / Anomaly Insights

Recommended visuals:

- Unknown airline count
- Missing airline count
- Quarantined flight count
- Quarantined payment count
- Payment invalid-rate percentage

---

## 15. Assumptions and Limitations

The following assumptions are important when interpreting the analysis:

- Flight duration is calculated from departure and arrival timestamps.
- Overnight flights are valid when the arrival timestamp occurs on the following calendar date.
- Temporal anomalies that cannot be logically resolved are quarantined.
- Missing or UNKNOWN airline values are retained as data-quality categories rather than being guessed or automatically corrected.
- Payment records with missing or unparseable amounts are excluded from valid payment analytics.
- Total Payment Value is **not treated as revenue** because transaction semantics and payment status are unavailable.
- Conventional flight delay metrics cannot be calculated from the available timestamp fields.
- The analysis is based on the provided dataset and therefore represents the characteristics of this dataset rather than real-world airline-wide performance.

---

## 16. Conclusion

The ASG Airlines pipeline converts inconsistent source data into validated analytical datasets while preserving data-quality visibility through flags and quarantine layers.

The resulting Gold layer supports measurable analysis of:

- Flight duration
- Overnight operations
- Route traffic
- Airline distribution
- Booking status
- Payment transaction quality
- Operational anomalies

The quantitative results demonstrate that the pipeline is not only performing data cleaning but also producing structured metrics that can be consumed directly by BI reporting and used for operational analysis.