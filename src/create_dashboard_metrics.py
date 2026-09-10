from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DOCS_DIR = PROJECT_ROOT / "docs"


# ---------------------------------------------------------
# Input files
# ---------------------------------------------------------

KPI_FILE = GOLD_DIR / "kpi_summary.csv"
QUALITY_FILE = DOCS_DIR / "data_quality_report.csv"
FLIGHTS_FILE = GOLD_DIR / "fact_flights.csv"
BOOKINGS_FILE = GOLD_DIR / "fact_bookings.csv"
PAYMENTS_FILE = GOLD_DIR / "fact_payments.csv"

OUTPUT_FILE = GOLD_DIR / "dashboard_metrics.csv"


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def add_metric(metrics, category, metric, value, unit=""):
    metrics.append(
        {
            "category": category,
            "metric": metric,
            "value": value,
            "unit": unit,
        }
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("Loading analytical datasets...")

    kpi = pd.read_csv(KPI_FILE)
    quality = pd.read_csv(QUALITY_FILE)
    flights = pd.read_csv(FLIGHTS_FILE)
    bookings = pd.read_csv(BOOKINGS_FILE)
    payments = pd.read_csv(PAYMENTS_FILE)

    metrics = []

    # -----------------------------------------------------
    # Business KPIs
    # -----------------------------------------------------

    for _, row in kpi.iterrows():

        add_metric(
            metrics,
            "Business KPI",
            row["kpi"],
            row["value"]
        )

    # -----------------------------------------------------
    # Data Quality Metrics
    # -----------------------------------------------------

    for _, row in quality.iterrows():

        metric_name = f"{row['dataset']} - {row['metric']}"

        add_metric(
            metrics,
            "Data Quality",
            metric_name,
            row["value"]
        )

    # -----------------------------------------------------
    # Additional Analytical KPIs
    # -----------------------------------------------------

    valid_flights = len(flights)
    valid_bookings = len(bookings)
    valid_payments = len(payments)

    # Flights per booking
    if valid_bookings > 0:
        flights_per_booking = valid_flights / valid_bookings
    else:
        flights_per_booking = 0

    add_metric(
        metrics,
        "Analytical KPI",
        "Flights per Booking",
        round(flights_per_booking, 2),
        "ratio"
    )

    # Payments per booking
    if valid_bookings > 0:
        payments_per_booking = valid_payments / valid_bookings
    else:
        payments_per_booking = 0

    add_metric(
        metrics,
        "Analytical KPI",
        "Payments per Booking",
        round(payments_per_booking, 2),
        "ratio"
    )

    # Average payment amount
    if valid_payments > 0:
        average_payment = payments["payment_amount"].mean()
    else:
        average_payment = 0

    add_metric(
        metrics,
        "Analytical KPI",
        "Average Payment Amount",
        round(average_payment, 2),
        "currency"
    )

    # Maximum flight duration
    if valid_flights > 0:
        max_duration = flights["flight_duration_minutes"].max()
    else:
        max_duration = 0

    add_metric(
        metrics,
        "Analytical KPI",
        "Maximum Flight Duration",
        round(max_duration, 2),
        "minutes"
    )

    # Minimum flight duration
    if valid_flights > 0:
        min_duration = flights["flight_duration_minutes"].min()
    else:
        min_duration = 0

    add_metric(
        metrics,
        "Analytical KPI",
        "Minimum Flight Duration",
        round(min_duration, 2),
        "minutes"
    )

    # -----------------------------------------------------
    # Overnight Flight Percentage
    # -----------------------------------------------------

    overnight_flag = (
        flights["overnight_flag"]
        .astype("string")
        .str.lower()
        .eq("true")
    )

    overnight_flights = overnight_flag.sum()

    if valid_flights > 0:
        overnight_percentage = (
            overnight_flights / valid_flights
        ) * 100
    else:
        overnight_percentage = 0

    add_metric(
        metrics,
        "Analytical KPI",
        "Overnight Flight Percentage",
        round(overnight_percentage, 2),
        "%"
    )

    # -----------------------------------------------------
    # Invalid Booking Percentage
    # -----------------------------------------------------

    invalid_booking_flag = (
        bookings["invalid_status_flag"]
        .astype("string")
        .str.lower()
        .eq("true")
    )

    invalid_bookings = invalid_booking_flag.sum()

    if valid_bookings > 0:
        invalid_booking_percentage = (
            invalid_bookings / valid_bookings
        ) * 100
    else:
        invalid_booking_percentage = 0

    add_metric(
        metrics,
        "Analytical KPI",
        "Invalid Booking Percentage",
        round(invalid_booking_percentage, 2),
        "%"
    )

    # -----------------------------------------------------
    # Create dashboard metrics table
    # -----------------------------------------------------

    dashboard_metrics = pd.DataFrame(metrics)

    dashboard_metrics.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("Dashboard metrics created successfully.")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Total dashboard metrics: {len(dashboard_metrics)}")

    print()
    print("Metric categories:")
    print(
        dashboard_metrics["category"]
        .value_counts()
    )


if __name__ == "__main__":
    main()