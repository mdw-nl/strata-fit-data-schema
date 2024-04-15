import pandas as pd
from pydantic import ValidationError, BaseModel
from typing import List

# Assuming 'Patient', 'ClinicalAssessment', ..., are your Pydantic models
from schema import Patient, ClinicalAssessment, Treatment, bDMARDTreatment, tsDMARDTreatment, PatientReportedOutcomes

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('synthetic_data.csv')

# Define a function to validate DataFrame rows against Pydantic models
def validate_df(df: pd.DataFrame, model: BaseModel) -> List[BaseModel]:
    validated_data = []
    errors = []
    for _, row in df.iterrows():
        try:
            validated_data.append(model(**row.to_dict()))
        except ValidationError as e:
            errors.append(e.json())
    return validated_data, errors

# Validate patient data
validated_patients, patient_errors = validate_df(df[['date_of_visit', 'date_of_birth', 'sex', 'date_of_RA_diagnosis']], Patient)
# Add more calls to `validate_df` for other parts of the DataFrame and corresponding models

if patient_errors:
    print("Validation errors found:", patient_errors)
else:
    print("All patient data is valid!")

# Repeat the validation for other segments of the DataFrame as needed, using the appropriate model for each segment.