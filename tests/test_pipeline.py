import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "quarantine"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"


def test_valid_flight_count():
    flights = pd.read_csv(PROCESSED_DIR / "flights_valid.csv")

    assert len(flights) == 1004


def test_flight_quarantine_count():
    quarantine = pd.read_csv(
        QUARANTINE_DIR / "flights_quarantine.csv"
    )

    assert len(quarantine) == 1


def test_valid_payment_count():
    payments = pd.read_csv(PROCESSED_DIR / "payments_valid.csv")

    assert len(payments) == 922


def test_payment_quarantine_count():
    quarantine = pd.read_csv(
        QUARANTINE_DIR / "payments_quarantine.csv"
    )

    assert len(quarantine) == 78


def test_no_orphan_booking_passenger_references():
    bookings = pd.read_csv(
        PROCESSED_DIR / "bookings_cleaned.csv"
    )
    passengers = pd.read_csv(
        PROCESSED_DIR / "passengers_cleaned.csv"
    )

    passenger_ids = set(
        passengers["passenger_id"].dropna()
    )

    booking_passenger_ids = set(
        bookings["passenger_id"].dropna()
    )

    assert booking_passenger_ids.issubset(passenger_ids)


def test_no_orphan_booking_flight_references():
    bookings = pd.read_csv(
        PROCESSED_DIR / "bookings_cleaned.csv"
    )

    valid_flights = pd.read_csv(
        PROCESSED_DIR / "flights_valid.csv"
    )

    quarantined_flights = pd.read_csv(
        QUARANTINE_DIR / "flights_quarantine.csv"
    )

    valid_flight_ids = set(
        valid_flights["flight_id"].dropna()
    )

    quarantined_flight_ids = set(
        quarantined_flights["flight_id"].dropna()
    )

    known_flight_ids = (
        valid_flight_ids | quarantined_flight_ids
    )

    booking_flight_ids = set(
        bookings["flight_id"].dropna()
    )

    assert booking_flight_ids.issubset(known_flight_ids)


def test_no_orphan_payment_booking_references():
    payments = pd.read_csv(
        PROCESSED_DIR / "payments_valid.csv"
    )
    bookings = pd.read_csv(
        PROCESSED_DIR / "bookings_cleaned.csv"
    )

    booking_ids = set(
        bookings["booking_id"].dropna()
    )

    payment_booking_ids = set(
        payments["booking_id"].dropna()
    )

    assert payment_booking_ids.issubset(booking_ids)


def test_gold_tables_exist():
    expected_tables = [
        "fact_flights.csv",
        "fact_bookings.csv",
        "fact_payments.csv",
        "route_summary.csv",
        "airline_summary.csv",
        "booking_summary.csv",
        "payment_summary.csv",
        "kpi_summary.csv",
        "dashboard_metrics.csv",
    ]

    for table in expected_tables:
        assert (GOLD_DIR / table).exists()


def test_gold_flight_count():
    flights = pd.read_csv(
        GOLD_DIR / "fact_flights.csv"
    )

    assert len(flights) == 1004


def test_gold_payment_count():
    payments = pd.read_csv(
        GOLD_DIR / "fact_payments.csv"
    )

    assert len(payments) == 922


def test_dashboard_metrics_count():
    metrics = pd.read_csv(
        GOLD_DIR / "dashboard_metrics.csv"
    )

    assert len(metrics) == 33