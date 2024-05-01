from datetime import date
from typing import Optional
from pydantic import BaseModel, validator, Field
from pydantic import conint, confloat

class Patient(BaseModel):
    date_of_visit: date = Field(..., example="2024-01-01")
    date_of_birth: date = Field(..., example="1980-12-01")
    sex: conint(ge=0, le=1) = Field(..., example=1)
    date_of_RA_diagnosis: date = Field(..., example="2010-01-01")
    
    @validator('date_of_birth', 'date_of_RA_diagnosis', pre=True)
    def date_not_in_future(cls, v, values, **kwargs):
        if v > date.today():
            raise ValueError(f"{values['field']} must not be in the future")
        return v

class ClinicalAssessment(BaseModel):
    RF_positivity: conint(ge=0, le=1) = Field(..., example=1)
    anti_CCP_positivity: conint(ge=0, le=1) = Field(..., example=0)
    DAS28_ESR: confloat(ge=0) = Field(..., example=2.3)
    patient_global: confloat(ge=0, le=100) = Field(..., example=70.0)
    patient_pain: confloat(ge=0, le=100) = Field(..., example=65.0)
    physician_global: confloat(ge=0, le=100) = Field(..., example=68.0)
    CRP: confloat(ge=0) = Field(..., example=1.5)
    ESR: conint(ge=0) = Field(..., example=25)
    SJC28: conint(ge=0, le=28) = Field(..., example=5)
    TJC28: conint(ge=0, le=28) = Field(..., example=3)

class Treatment(BaseModel):
    concomitant_csDMARDs: conint(ge=0, le=1) = Field(..., example=1)
    type_of_concomitant_csDMARD: Optional[conint(ge=1, le=5)] = Field(default=None, example=3)
    dose_of_concomitant_csDMARDs: Optional[confloat(ge=0)] = Field(default=None, example=10.0)
    N_previous_csDMARDs: conint(ge=0) = Field(..., example=2)

class bDMARDTreatment(BaseModel):
    current_bDMARD_type: conint(ge=1, le=5) = Field(..., example=4)
    start_date_current_bDMARD: date = Field(..., example="2023-02-01")
    stop_date_current_bDMARD: Optional[date] = Field(default=None, example="2024-02-01")
    if_stop_reason: Optional[conint(ge=1, le=4)] = Field(default=None, example=2)
    
    @validator('stop_date_current_bDMARD', pre=True)
    def stop_date_after_start_date(cls, v, values, **kwargs):
        if 'start_date_current_bDMARD' in values and v is not None:
            if v < values['start_date_current_bDMARD']:
                raise ValueError("stop_date must be after start date")
        return v

class tsDMARDTreatment(BaseModel):
    current_tsDMARD_type: conint(ge=1, le=4) = Field(..., example=1)
    start_date_current_tsDMARD: date = Field(..., example="2023-04-01")
    stop_date_current_tsDMARD: Optional[date] = Field(default=None, example="2024-04-01")
    if_stop_reason: Optional[conint(ge=1, le=4)] = Field(default=None, example=3)

class PatientReportedOutcomes(BaseModel):
    EQ5D: Optional[confloat(ge=0)] = Field(default=None, example=0.85)
    HAQ: Optional[confloat(ge=0, le=3)] = Field(default=None, example=2.1)
