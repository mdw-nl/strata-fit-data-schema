import pandas as pd
import numpy as np
import argparse
from datetime import date
from pydantic import ValidationError
from schema import PatientData, ValidationDetail

def get_date_fields(model) -> list[str]:
    """Retrieve a list of field names where the type is datetime.date."""
    return [field_name for field_name, field_type in model.__annotations__.items()
            if field_type == date]

def validate_csv(df):
    # Existing logic remains largely the same
    date_fields = get_date_fields(PatientData)
    for field in date_fields:
        if field in df.columns:
            df[field] = pd.to_datetime(df[field], errors='coerce')
            df[field] = df[field].apply(lambda x: x if pd.notnull(x) else None)

    errors = []
    for index, row in df.iterrows():
        try:
            row_dict = row.where(pd.notnull(row), None).to_dict()
            patient_data = PatientData(**row_dict)
        except ValidationError as e:
            errors.append({'row': index, 'errors': e.errors()})
    return errors


def translate_errors(errors):
    descriptions = {
        "date_of_birth": "Date of birth should be in the format: day/month/year.",
        "sex": "Sex should be 0 for male or 1 for female.",
        "patient_global": "Patient global score should be between 0 and 100.",
        "RF_positivity": "RF positivity should be 0 for negative or 1 for positive.",
        "DAS28_ESR": "DAS28-ESR should be a numeric value with up to 2 decimal places.",
        "if_stop_reason": "Reason for stopping should be one of: 1 for inefficacy, 2 for intolerance, 3 for remission, 4 for other/unknown."
    }
    readable_errors = []
    for error in errors:
        field = error['loc'][0]
        message = descriptions.get(field, error['msg'])
        error_type = error['type']
        input_value = str(error.get('input', 'N/A'))  # Ensure value is a string for Pydantic compatibility
        readable_errors.append(ValidationDetail(
            field=field,
            message=message,
            error_type=error_type,
            input_value=input_value
        ))
    return readable_errors



def main():
    parser = argparse.ArgumentParser(description="Validate CSV data against the Pydantic model")
    parser.add_argument('filepath', type=str, help='Path to the CSV file to validate')
    args = parser.parse_args()

    # Validate the provided CSV file
    df = pd.read_csv(args.filepath)
    validation_errors = validate_csv(df)

    if validation_errors:
        print("Validation Errors:")
        for error in validation_errors:
            print(f"Row {error['row']}:")
            for detail in error['errors']:
                print(f"  {detail['loc'][0]}: {detail['msg']}")
    else:
        print("No validation errors found.")

if __name__ == "__main__":
    main()