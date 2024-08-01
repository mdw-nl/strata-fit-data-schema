from functools import lru_cache
from fastapi import FastAPI, Response, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
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
    contact=settings.openapi.contact
)

@app.get("/settings", tags=["Settings"])
def get_settings():
    settings_file_path = settings.openapi.settings_path
    if os.path.exists(settings_file_path):
        return FileResponse(settings_file_path)
    else:
        return Response(content="Settings file not found.", status_code=404)

@lru_cache
def get_models():
    return logic.load_data_models_from_settings()

@app.post("/validate", tags=["Validation"])
async def validate_csv_file(file: UploadFile = File(...), models: dict = Depends(get_models)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    try:
        data = await file.read()
        df = pd.read_csv(io.StringIO(data.decode('utf-8')))
        model_name = "PatientData"  # Example, you can dynamically determine this
        model = models[model_name]
        has_errors, errors = logic.validate_csv(df, model)

        if has_errors:
            return ValidationReport(errors=errors)
        else:
            return JSONResponse(content={"message": "Data validated - no errors found"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

