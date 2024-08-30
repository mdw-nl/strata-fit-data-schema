from functools import lru_cache
from fastapi import FastAPI, Response, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
import pandas as pd
import io
import os
import logging

from config.config import settings
from api.schema import ValidationReport, PandasDelimeter
from api.logic import validate_csv, load_data_models_from_settings
from api.logs import setup_logging
from api.utils import pretty_format_model

# Setup the logging
logger = logging.getLogger(__name__)
setup_logging(level=settings.logging.level)

# Initialize the Validator App
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
        logger.info(f"Settings file retrieved: {settings_file_path}")
        with open(settings_file_path, 'r') as settings_file:
            return Response(content=settings_file.read(), media_type="application/x-yaml")
    else:
        logger.warning(f"Settings file not found at: {settings_file_path}")
        return Response(content="Settings file not found.", status_code=404)
    
@app.get("/schema", tags=["Settings"])
def get_schema():
    schema_file_path = settings.openapi.schema_path
    if os.path.exists(schema_file_path):
        logger.info(f"Schema file retrieved: {schema_file_path}")
        with open(schema_file_path, 'r') as schema_file:
            return Response(content=schema_file.read(), media_type="application/x-yaml")
    else:
        logger.warning(f"Schema file not found at: {schema_file_path}")
        return Response(content="Data Schema file not found.", status_code=404)

@lru_cache
def get_models():
    models = load_data_models_from_settings()
    pretty_models = "\n".join(
        pretty_format_model(model_name, model) for model_name, model in models.items()
    )
    logger.info(f"Data models loaded:{pretty_models}")
    return models

@app.post("/validate", tags=["Validation"])
async def validate_csv_file(
    file: UploadFile = File(...),
    delimeter: PandasDelimeter = PandasDelimeter.COMMA,
    models: dict = Depends(get_models)):
    if not file.filename.endswith('.csv'):
        logger.error(f"Invalid file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    try:
        data = await file.read()
        df = pd.read_csv(io.StringIO(data.decode('utf-8')), delimiter=delimeter.value)
        model_name = "PatientData"  # Example, you can dynamically determine this
        model = models[model_name]
        has_errors, errors = validate_csv(df, model)

        if has_errors:
            logger.info(f"Validation failed with errors: {errors}")
            return ValidationReport(errors=errors)
        else:
            logger.info("Data validated successfully, no errors found.")
            return JSONResponse(content={"message": "Data validated - no errors found"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

