from fastapi import FastAPI, Response, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import io
import os

from config.config import settings
from schema import ValidationReport
import logic


app = FastAPI(
    title=settings.openapi.title,
    description=settings.openapi.description,
    version=settings.openapi.version,
    lifespan=None,
    contact=settings.openapi.contact
)


@app.get("/settings", tags=["Validation"])
def get_settings():
    settings_file_path = settings.openapi.settings_path
    if os.path.exists(settings_file_path):
        return FileResponse(settings_file_path)
    else:
        return Response(content="Settings file not found.", status_code=404)


@app.post("/validate", response_model=ValidationReport, tags=["Validation"])
async def validate_csv_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    try:
        data = await file.read()
        df = pd.read_csv(io.StringIO(data.decode('utf-8')))
        raw_errors = logic.validate_csv(df)

        # Flatten the list of translated error details
        errors = []
        for error in raw_errors:
            translated_errors = logic.translate_errors(error['errors'])
            errors.extend(translated_errors)  # Extend the main list with the sublist items

        return ValidationReport(errors=errors)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


