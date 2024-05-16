from datetime import date

from old.nested_schema import Patient

# Example usage
if __name__ == "__main__":
    patient_example = Patient(
        date_of_visit=date(2022, 9, 12),
        date_of_birth=date(1980, 6, 15),
        sex=1,
        date_of_RA_diagnosis=date(2019, 3, 10)
    )
    print(patient_example)
