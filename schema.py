from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Union

class ValidationDetail(BaseModel):
    row: Union[int, str]
    field: str
    message: str
    error_type: str
    input_value: str

class ValidationReport(BaseModel):
    errors: Optional[list[ValidationDetail]] = None


class PatientData(BaseModel):
    date_of_visit: date = Field(..., example="2024-01-01")
    date_of_birth: date = Field(..., example="1980-12-01")
    sex: int = Field(..., ge=0, le=1, example=1)
    date_of_RA_diagnosis: date = Field(..., example="2010-01-01")
    RF_positivity: int = Field(..., ge=0, le=1, example=1)
    anti_CCP_positivity: int = Field(..., ge=0, le=1, example=0)
    DAS28_ESR: float = Field(..., example=2.5)
    patient_global: float = Field(..., ge=0, le=100, example=75.0)
    patient_pain: float = Field(..., ge=0, le=100, example=65.0)
    physician_global: float = Field(..., ge=0, le=100, example=70.0)
    CRP: float = Field(..., example=1.2)
    ESR: int = Field(..., example=20)
    SJC28: int = Field(..., ge=0, le=28, example=4)
    TJC28: int = Field(..., ge=0, le=28, example=6)
    concomitant_csDMARDs: int = Field(..., ge=0, le=1, example=1)
    type_of_concomitant_csDMARD: Optional[int] = Field(None, ge=1, le=5, example=3)
    dose_of_concomitant_csDMARDs: Optional[float] = Field(None, example=50.0)
    N_previous_csDMARDs: int = Field(..., example=2)
    current_bDMARD_type: Optional[int] = Field(None, ge=1, le=5, example=2)
    start_date_current_bDMARD: Optional[date] = Field(None, example="2023-01-01")
    stop_date_current_bDMARD: Optional[date] = Field(None, example="2024-01-01")
    if_stop_reason: Optional[int] = Field(None, ge=1, le=4, example=1)
    number_of_prior_bDMARDs: Optional[int] = Field(None, example=1)
    current_tsDMARD_type: Optional[int] = Field(None, ge=1, le=4, example=4)
    start_date_current_tsDMARD: Optional[date] = Field(None, example="2023-02-01")
    stop_date_current_tsDMARD: Optional[date] = Field(None, example="2024-02-01")
    if_stop_reason_tsDMARD: Optional[int] = Field(None, ge=1, le=4, example=2)
    number_of_prior_tsDMARDs: Optional[int] = Field(None, example=3)
    concomitant_GCs: Optional[int] = Field(None, ge=0, le=1, example=0)
    type_of_concomitant_GCs: Optional[str] = Field(None, example="Prednisone")
    dose_of_concomitant_GCs: Optional[float] = Field(None, example=5.0)
    EQ5D: Optional[float] = Field(None, example=0.85)
    HAQ: Optional[float] = Field(None, ge=0, le=3, example=1.25)
