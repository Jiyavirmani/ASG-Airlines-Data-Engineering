import os
import pandas as pd



# Paths

RAW_FILE = "data/raw/UseCase - Airlines.xlsx"
PROCESSED_DIR = "data/processed"
QUARANTINE_DIR = "data/quarantine"



# Setup

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(QUARANTINE_DIR, exist_ok=True)



# Load data


def load_data():
    print("Loading Excel workbook...")

    flights = pd.read_excel(RAW_FILE, sheet_name="flights")
    bookings = pd.read_excel(RAW_FILE, sheet_name="bookings")
    passengers = pd.read_excel(RAW_FILE, sheet_name="passengers")
    payments = pd.read_excel(RAW_FILE, sheet_name="payments")

    return flights, bookings, passengers, payments


# Clean Flights


def clean_flights(df):

    print("\nCleaning flights...")

    # Remove completely empty rows
    df = df.dropna(how="all").copy()

    # Keep only required columns
    df = df[
        [
            "flight_id",
            "airline",
            "source",
            "destination",
            "departure_time",
            "arrival_time",
            "duration",
        ]
    ]

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Standardize text columns
    text_columns = [
        "flight_id",
        "airline",
        "source",
        "destination",
    ]

    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()

    # Handle missing airline
    df["airline_missing_flag"] = df["airline"].isna()

    df["airline"] = df["airline"].fillna("UNKNOWN")

    # Preserve existing UNKNOWN values
    df["airline_unknown_flag"] = (
        df["airline"].str.upper() == "UNKNOWN"
    )

    # Convert timestamps
    df["departure_time"] = pd.to_datetime(
        df["departure_time"],
        errors="coerce"
    )

    df["arrival_time"] = pd.to_datetime(
        df["arrival_time"],
        errors="coerce"
    )

    # Flag invalid timestamps
    df["invalid_timestamp_flag"] = (
        df["departure_time"].isna()
        | df["arrival_time"].isna()
    )

    # Calculate duration from timestamps
    df["calculated_duration_minutes"] = (
        df["arrival_time"] - df["departure_time"]
    ).dt.total_seconds() / 60

    # Flag arrival before departure
    df["temporal_anomaly_flag"] = (
        df["calculated_duration_minutes"] < 0
    )

    # Flag overnight flights
    df["overnight_flag"] = (
        df["departure_time"].dt.date
        != df["arrival_time"].dt.date
    )

    # Compare source duration where possible
    source_duration = pd.to_timedelta(
        df["duration"].astype("string"),
        errors="coerce"
    )

    df["source_duration_minutes"] = (
        source_duration.dt.total_seconds() / 60
    )

    df["duration_difference_minutes"] = (
        df["calculated_duration_minutes"]
        - df["source_duration_minutes"]
    )

    # Duration mismatch tolerance: 1 minute
    df["duration_mismatch_flag"] = (
        df["duration_difference_minutes"].abs() > 1
    )

    return df



# Clean Bookings


def clean_bookings(df):

    print("Cleaning bookings...")

    # Remove completely empty rows
    df = df.dropna(how="all").copy()

    # Remove exact duplicates
    df = df.drop_duplicates()

    # Standardize text fields
    text_columns = [
        "booking_id",
        "passenger_id",
        "flight_id",
        "status",
        "seat_number",
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # Standardize booking status
    df["status"] = df["status"].str.upper()

    # Flag missing/invalid status
    valid_statuses = {
        "CONFIRMED",
        "CANCELLED",
        "PENDING",
        "INVALID",
    }

    df["invalid_status_flag"] = (
        df["status"].isna()
        | ~df["status"].isin(valid_statuses)
    )

    return df



# Clean Passengers


def clean_passengers(df):

    print("Cleaning passengers...")

    df = df.dropna(how="all").copy()

    # Remove exact duplicates
    df = df.drop_duplicates()

    # Standardize text fields
    text_columns = [
        "passenger_id",
        "first_name",
        "last_name",
        "gender",
        "email",
        "phone",
        "aadhaar_id",
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # Standardize gender
    df["gender"] = df["gender"].str.upper()

    # Convert DOB
    if "date_of_birth" in df.columns:
        df["date_of_birth"] = pd.to_datetime(
            df["date_of_birth"],
            errors="coerce"
        )

    return df



# Clean Payments


def clean_payments(df):

    print("Cleaning payments...")

    df = df.dropna(how="all").copy()

    # Remove exact duplicates
    df = df.drop_duplicates()

    # Standardize text
    text_columns = [
        "payment_id",
        "booking_id",
        "payment_method",
    ]

    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()

    # Standardize payment method
    df["payment_method"] = df["payment_method"].str.upper()

    # Convert amount
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Flag invalid amounts
    df["invalid_amount_flag"] = (
        df["amount"].isna()
        | (df["amount"] <= 0)
    )

    return df



# Referential Integrity


def validate_relationships(
    flights,
    bookings,
    passengers,
    payments
):

    print("\nValidating relationships...")

    valid_flight_ids = set(
        flights["flight_id"].dropna()
    )

    valid_passenger_ids = set(
        passengers["passenger_id"].dropna()
    )

    valid_booking_ids = set(
        bookings["booking_id"].dropna()
    )

    bookings["orphan_passenger_flag"] = (
        bookings["passenger_id"].notna()
        & ~bookings["passenger_id"].isin(valid_passenger_ids)
    )

    bookings["orphan_flight_flag"] = (
        bookings["flight_id"].notna()
        & ~bookings["flight_id"].isin(valid_flight_ids)
    )

    payments["orphan_booking_flag"] = (
        payments["booking_id"].notna()
        & ~payments["booking_id"].isin(valid_booking_ids)
    )

    return bookings, payments



# Save Data


def save_data(
    flights,
    bookings,
    passengers,
    payments
):

    print("\nSaving cleaned datasets...")

    flights.to_csv(
        f"{PROCESSED_DIR}/flights_cleaned.csv",
        index=False
    )

    bookings.to_csv(
        f"{PROCESSED_DIR}/bookings_cleaned.csv",
        index=False
    )

    passengers.to_csv(
        f"{PROCESSED_DIR}/passengers_cleaned.csv",
        index=False
    )

    payments.to_csv(
        f"{PROCESSED_DIR}/payments_cleaned.csv",
        index=False
    )

    print("Files saved successfully.")


# Main Pipeline


def main():

    flights, bookings, passengers, payments = load_data()

    flights = clean_flights(flights)
    bookings = clean_bookings(bookings)
    passengers = clean_passengers(passengers)
    payments = clean_payments(payments)

    bookings, payments = validate_relationships(
        flights,
        bookings,
        passengers,
        payments
    )

    save_data(
        flights,
        bookings,
        passengers,
        payments
    )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()