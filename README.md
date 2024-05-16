# STRATA-FIT Data Validation App

## Project Description
The Strata-Fit Data Validation Application is a FastAPI-based tool designed to ensure the quality and integrity of CSV data files containing clinical information about patients with rheumatoid arthritis (RA). This application leverages a Pydantic model (PatientData) to validate the data against a predefined schema ensuring it meets specific criteria, such as data type, value range, and required fields.

The application supports file uploads through an API endpoint where users can submit their CSV files to be validated. Errors and discrepancies are reported back in a user-friendly format, making it easier for clinicians and researchers to identify and correct data issues.

## Data Diagrams (PlantUML)
### App
![app](docs/app.png)