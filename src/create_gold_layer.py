import os
import pandas as pd


PROCESSED_DIR = "data/processed"
GOLD_DIR = "data/gold"


os.makedirs(GOLD_DIR, exist_ok=True)


# ---------------------------------------------------------
# Load cleaned data
# ---------------------------------------------------------

def load_data():

    flights = pd.read_csv(
        f"{PROCESSED_DIR}/flights_valid.csv"
    )

    bookings = pd.read_csv(
        f"{PROCESSED_DIR}/bookings_cleaned.csv"
    )

    passengers = pd.read_csv(
        f"{PROCESSED_DIR}/passengers_cleaned.csv"
    )

    payments = pd.read_csv(
        f"{PROCESSED_DIR}/payments_valid.csv"
    )

    return flights, bookings, passengers, payments


# ---------------------------------------------------------
# Flight Fact Table
# ---------------------------------------------------------

def create_flight_fact(flights):

    fact_flights = flights.copy()

    # Convert timestamps
    fact_flights["departure_time"] = pd.to_datetime(
        fact_flights["departure_time"]
    )

    fact_flights["arrival_time"] = pd.to_datetime(
        fact_flights["arrival_time"]
    )

    # Analytical duration
    fact_flights["flight_duration_minutes"] = (
        fact_flights["arrival_time"]
        - fact_flights["departure_time"]
    ).dt.total_seconds() / 60

    # Route
    fact_flights["route"] = (
        fact_flights["source"]
        + " → "
        + fact_flights["destination"]
    )

    # Flight date
    fact_flights["departure_date"] = (
        fact_flights["departure_time"].dt.date
    )

    return fact_flights


# ---------------------------------------------------------
# Booking Fact Table
# ---------------------------------------------------------

def create_booking_fact(bookings):

    fact_bookings = bookings.copy()

    # Booking status categories
    fact_bookings["is_confirmed"] = (
        fact_bookings["status"] == "CONFIRMED"
    )

    fact_bookings["is_cancelled"] = (
        fact_bookings["status"] == "CANCELLED"
    )

    fact_bookings["is_pending"] = (
        fact_bookings["status"] == "PENDING"
    )

    fact_bookings["is_invalid"] = (
        fact_bookings["status"] == "INVALID"
    )

    return fact_bookings


# ---------------------------------------------------------
# Payment Fact Table
# ---------------------------------------------------------

def create_payment_fact(payments):

    fact_payments = payments.copy()

    fact_payments["payment_amount"] = pd.to_numeric(
        fact_payments["amount"],
        errors="coerce"
    )

    return fact_payments


# ---------------------------------------------------------
# Route Performance
# ---------------------------------------------------------

def create_route_summary(flights):

    route_summary = (
        flights
        .groupby(
            ["source", "destination", "route"],
            as_index=False
        )
        .agg(
            total_flights=("flight_id", "count"),
            average_duration_minutes=(
                "flight_duration_minutes",
                "mean"
            ),
            median_duration_minutes=(
                "flight_duration_minutes",
                "median"
            ),
            overnight_flights=(
                "overnight_flag",
                "sum"
            )
        )
    )

    route_summary["overnight_percentage"] = (
        route_summary["overnight_flights"]
        / route_summary["total_flights"]
        * 100
    )

    return route_summary


# ---------------------------------------------------------
# Airline Summary
# ---------------------------------------------------------

def create_airline_summary(flights):

    airline_summary = (
        flights
        .groupby("airline", as_index=False)
        .agg(
            total_flights=("flight_id", "count"),
            average_duration_minutes=(
                "flight_duration_minutes",
                "mean"
            ),
            median_duration_minutes=(
                "flight_duration_minutes",
                "median"
            ),
            overnight_flights=(
                "overnight_flag",
                "sum"
            )
        )
    )

    airline_summary["flight_share_percentage"] = (
        airline_summary["total_flights"]
        / airline_summary["total_flights"].sum()
        * 100
    )

    return airline_summary


# ---------------------------------------------------------
# Booking Summary
# ---------------------------------------------------------

def create_booking_summary(bookings):

    booking_summary = (
        bookings["status"]
        .value_counts()
        .reset_index()
    )

    booking_summary.columns = [
        "status",
        "total_bookings"
    ]

    booking_summary["percentage"] = (
        booking_summary["total_bookings"]
        / booking_summary["total_bookings"].sum()
        * 100
    )

    return booking_summary


# ---------------------------------------------------------
# Payment Summary
# ---------------------------------------------------------

def create_payment_summary(payments):

    payment_summary = (
        payments
        .groupby("payment_method", as_index=False)
        .agg(
            total_transactions=(
                "payment_id",
                "count"
            ),
            total_amount=(
                "payment_amount",
                "sum"
            ),
            average_payment_amount=(
                "payment_amount",
                "mean"
            )
        )
    )

    return payment_summary


# ---------------------------------------------------------
# Overall KPI Summary
# ---------------------------------------------------------

def create_kpi_summary(
    flights,
    bookings,
    payments
):

    total_flights = len(flights)
    total_bookings = len(bookings)
    total_payments = len(payments)

    confirmed = (
        bookings["status"] == "CONFIRMED"
    ).sum()

    cancelled = (
        bookings["status"] == "CANCELLED"
    ).sum()

    pending = (
        bookings["status"] == "PENDING"
    ).sum()

    kpi = pd.DataFrame([
        {
            "kpi": "Total Flights",
            "value": total_flights
        },
        {
            "kpi": "Total Bookings",
            "value": total_bookings
        },
        {
            "kpi": "Valid Payment Transactions",
            "value": total_payments
        },
        {
            "kpi": "Average Flight Duration (Minutes)",
            "value": flights[
                "flight_duration_minutes"
            ].mean()
        },
        {
            "kpi": "Median Flight Duration (Minutes)",
            "value": flights[
                "flight_duration_minutes"
            ].median()
        },
        {
            "kpi": "Overnight Flights",
            "value": flights[
                "overnight_flag"
            ].sum()
        },
        {
            "kpi": "Confirmed Booking Rate (%)",
            "value": confirmed
            / total_bookings
            * 100
        },
        {
            "kpi": "Cancellation Rate (%)",
            "value": cancelled
            / total_bookings
            * 100
        },
        {
            "kpi": "Pending Booking Rate (%)",
            "value": pending
            / total_bookings
            * 100
        },
        {
            "kpi": "Total Payment Value",
            "value": payments[
                "payment_amount"
            ].sum()
        }
    ])

    return kpi


# ---------------------------------------------------------
# Save Gold Tables
# ---------------------------------------------------------

def save_gold_tables(
    fact_flights,
    fact_bookings,
    fact_payments,
    route_summary,
    airline_summary,
    booking_summary,
    payment_summary,
    kpi_summary
):

    fact_flights.to_csv(
        f"{GOLD_DIR}/fact_flights.csv",
        index=False
    )

    fact_bookings.to_csv(
        f"{GOLD_DIR}/fact_bookings.csv",
        index=False
    )

    fact_payments.to_csv(
        f"{GOLD_DIR}/fact_payments.csv",
        index=False
    )

    route_summary.to_csv(
        f"{GOLD_DIR}/route_summary.csv",
        index=False
    )

    airline_summary.to_csv(
        f"{GOLD_DIR}/airline_summary.csv",
        index=False
    )

    booking_summary.to_csv(
        f"{GOLD_DIR}/booking_summary.csv",
        index=False
    )

    payment_summary.to_csv(
        f"{GOLD_DIR}/payment_summary.csv",
        index=False
    )

    kpi_summary.to_csv(
        f"{GOLD_DIR}/kpi_summary.csv",
        index=False
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("Creating Gold analytical layer...\n")

    flights, bookings, passengers, payments = load_data()

    fact_flights = create_flight_fact(flights)

    fact_bookings = create_booking_fact(bookings)

    fact_payments = create_payment_fact(payments)

    route_summary = create_route_summary(
        fact_flights
    )

    airline_summary = create_airline_summary(
        fact_flights
    )

    booking_summary = create_booking_summary(
        fact_bookings
    )

    payment_summary = create_payment_summary(
        fact_payments
    )

    kpi_summary = create_kpi_summary(
        fact_flights,
        fact_bookings,
        fact_payments
    )

    save_gold_tables(
        fact_flights,
        fact_bookings,
        fact_payments,
        route_summary,
        airline_summary,
        booking_summary,
        payment_summary,
        kpi_summary
    )

    print("Gold layer created successfully.")

    print("\nGenerated tables:")

    print("- fact_flights.csv")
    print("- fact_bookings.csv")
    print("- fact_payments.csv")
    print("- route_summary.csv")
    print("- airline_summary.csv")
    print("- booking_summary.csv")
    print("- payment_summary.csv")
    print("- kpi_summary.csv")


if __name__ == "__main__":
    main()