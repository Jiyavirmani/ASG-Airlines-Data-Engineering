import pandas as pd


RAW_FILE = "data/raw/UseCase - Airlines.xlsx"


def main():

    print("Loading raw data for verification...\n")

    passengers = pd.read_excel(
        RAW_FILE,
        sheet_name="passengers"
    )

    payments = pd.read_excel(
        RAW_FILE,
        sheet_name="payments"
    )

    # -----------------------------------------------------
    # Passenger DOB verification
    # -----------------------------------------------------

    print("PASSENGER DOB CHECK")
    print("-------------------")

    print(
        "Raw passenger rows:",
        len(passengers)
    )

    print(
        "Raw missing DOB:",
        passengers["date_of_birth"].isna().sum()
    )

    print(
        "Raw blank-string DOB:",
        (
            passengers["date_of_birth"]
            .astype("string")
            .str.strip()
            .eq("")
            .sum()
        )
    )

    parsed_dob = pd.to_datetime(
        passengers["date_of_birth"],
        errors="coerce"
    )

    print(
        "Unparseable DOB after conversion:",
        parsed_dob.isna().sum()
    )

    # -----------------------------------------------------
    # Payment amount verification
    # -----------------------------------------------------

    print("\nPAYMENT AMOUNT CHECK")
    print("--------------------")

    print(
        "Raw payment rows:",
        len(payments)
    )

    raw_missing = payments["amount"].isna()

    print(
        "Missing payment amounts:",
        raw_missing.sum()
    )

    numeric_amount = pd.to_numeric(
        payments["amount"],
        errors="coerce"
    )

    non_positive = (
        numeric_amount.notna()
        & (numeric_amount <= 0)
    )

    print(
        "Non-positive payment amounts:",
        non_positive.sum()
    )

    invalid_format = (
        numeric_amount.isna()
        & ~raw_missing
    )

    print(
        "Unparseable payment amounts:",
        invalid_format.sum()
    )

    total_invalid = (
        raw_missing
        | non_positive
        | invalid_format
    )

    print(
        "Total invalid payment amounts:",
        total_invalid.sum()
    )

    # -----------------------------------------------------
    # Show suspicious payment values
    # -----------------------------------------------------

    if non_positive.sum() > 0:

        print("\nNon-positive payment values:")

        print(
            payments.loc[
                non_positive,
                ["payment_id", "booking_id", "amount"]
            ].to_string(index=False)
        )

    if invalid_format.sum() > 0:

        print("\nUnparseable payment values:")

        print(
            payments.loc[
                invalid_format,
                ["payment_id", "booking_id", "amount"]
            ].to_string(index=False)
        )

    print("\nVerification completed.")


if __name__ == "__main__":
    main()