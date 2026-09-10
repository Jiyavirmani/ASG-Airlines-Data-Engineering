import pandas as pd


PROCESSED_DIR = "data/processed"
REPORT_FILE = "docs/data_quality_report.csv"


def count_true(df, column):
    if column not in df.columns:
        return 0
    return int(df[column].sum())


def main():

    flights = pd.read_csv(
        f"{PROCESSED_DIR}/flights_cleaned.csv"
    )

    bookings = pd.read_csv(
        f"{PROCESSED_DIR}/bookings_cleaned.csv"
    )

    passengers = pd.read_csv(
        f"{PROCESSED_DIR}/passengers_cleaned.csv"
    )

    payments = pd.read_csv(
        f"{PROCESSED_DIR}/payments_cleaned.csv"
    )

    report = [

        # Flights
        {
            "dataset": "flights",
            "metric": "total_records",
            "value": len(flights)
        },
        {
            "dataset": "flights",
            "metric": "missing_airline",
            "value": count_true(
                flights,
                "airline_missing_flag"
            )
        },
        {
            "dataset": "flights",
            "metric": "unknown_airline",
            "value": count_true(
                flights,
                "airline_unknown_flag"
            )
        },
        {
            "dataset": "flights",
            "metric": "invalid_timestamps",
            "value": count_true(
                flights,
                "invalid_timestamp_flag"
            )
        },
        {
            "dataset": "flights",
            "metric": "temporal_anomalies",
            "value": count_true(
                flights,
                "temporal_anomaly_flag"
            )
        },
        {
            "dataset": "flights",
            "metric": "overnight_flights",
            "value": count_true(
                flights,
                "overnight_flag"
            )
        },
        {
            "dataset": "flights",
            "metric": "duration_mismatches",
            "value": count_true(
                flights,
                "duration_mismatch_flag"
            )
        },

        # Bookings
        {
            "dataset": "bookings",
            "metric": "total_records",
            "value": len(bookings)
        },
        {
            "dataset": "bookings",
            "metric": "invalid_status",
            "value": count_true(
                bookings,
                "invalid_status_flag"
            )
        },
        {
            "dataset": "bookings",
            "metric": "orphan_passenger_references",
            "value": count_true(
                bookings,
                "orphan_passenger_flag"
            )
        },
        {
            "dataset": "bookings",
            "metric": "orphan_flight_references",
            "value": count_true(
                bookings,
                "orphan_flight_flag"
            )
        },

        # Passengers
        {
            "dataset": "passengers",
            "metric": "total_records",
            "value": len(passengers)
        },
        {
            "dataset": "passengers",
            "metric": "missing_date_of_birth",
            "value": int(
                passengers["date_of_birth"].isna().sum()
            )
        },

        # Payments
        {
            "dataset": "payments",
            "metric": "total_records",
            "value": len(payments)
        },
        {
            "dataset": "payments",
            "metric": "invalid_amount",
            "value": count_true(
                payments,
                "invalid_amount_flag"
            )
        },
        {
            "dataset": "payments",
            "metric": "orphan_booking_references",
            "value": count_true(
                payments,
                "orphan_booking_flag"
            )
        }
    ]

    report_df = pd.DataFrame(report)

    report_df.to_csv(
        REPORT_FILE,
        index=False
    )

    print("\nData Quality Report")
    print("===================")
    print(report_df.to_string(index=False))

    print(
        f"\nReport saved to: {REPORT_FILE}"
    )


if __name__ == "__main__":
    main()