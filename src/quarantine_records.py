import os
import pandas as pd


PROCESSED_DIR = "data/processed"
QUARANTINE_DIR = "data/quarantine"


# ---------------------------------------------------------
# Setup
# ---------------------------------------------------------

os.makedirs(QUARANTINE_DIR, exist_ok=True)


# ---------------------------------------------------------
# Quarantine Flights
# ---------------------------------------------------------

def process_flights():

    flights = pd.read_csv(
        f"{PROCESSED_DIR}/flights_cleaned.csv"
    )

    # Records that cannot safely be used for duration analysis
    quarantine_mask = (
        flights["invalid_timestamp_flag"].astype(bool)
        | flights["temporal_anomaly_flag"].astype(bool)
    )

    quarantine = flights[quarantine_mask].copy()

    valid = flights[~quarantine_mask].copy()

    quarantine["quarantine_reason"] = "INVALID_TIMESTAMP_OR_TEMPORAL_ANOMALY"

    quarantine.to_csv(
        f"{QUARANTINE_DIR}/flights_quarantine.csv",
        index=False
    )

    valid.to_csv(
        f"{PROCESSED_DIR}/flights_valid.csv",
        index=False
    )

    print("\nFlights")
    print("-------")
    print(f"Input records: {len(flights)}")
    print(f"Quarantined: {len(quarantine)}")
    print(f"Valid records: {len(valid)}")

    return flights, valid, quarantine


# ---------------------------------------------------------
# Quarantine Payments
# ---------------------------------------------------------

def process_payments():

    payments = pd.read_csv(
        f"{PROCESSED_DIR}/payments_cleaned.csv"
    )

    quarantine_mask = (
        payments["invalid_amount_flag"].astype(bool)
    )

    quarantine = payments[quarantine_mask].copy()

    valid = payments[~quarantine_mask].copy()

    quarantine["quarantine_reason"] = "INVALID_PAYMENT_AMOUNT"

    quarantine.to_csv(
        f"{QUARANTINE_DIR}/payments_quarantine.csv",
        index=False
    )

    valid.to_csv(
        f"{PROCESSED_DIR}/payments_valid.csv",
        index=False
    )

    print("\nPayments")
    print("--------")
    print(f"Input records: {len(payments)}")
    print(f"Quarantined: {len(quarantine)}")
    print(f"Valid records: {len(valid)}")

    return payments, valid, quarantine


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("Starting quarantine process...")

    process_flights()
    process_payments()

    print("\nQuarantine process completed.")


if __name__ == "__main__":
    main()