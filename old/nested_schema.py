from datetime import date
from typing import Optional
from pydantic import BaseModel, validator, Field
from pydantic import conint, confloat, constr

class Patient(BaseModel):
    date_of_visit: date = Field(...)
    date_of_birth: date = Field(...)
    sex: conint(ge=0, le=1) = Field(...)
    date_of_RA_diagnosis: date = Field(...)
    
    @validator('date_of_birth', 'date_of_RA_diagnosis', pre=True)
    def date_not_in_future(cls, v, values, **kwargs):
        if v > date.today():
            raise ValueError(f"{values['field']} must not be in the future")
        return v

class ClinicalAssessment(BaseModel):
    RF_positivity: conint(ge=0, le=1) = Field(...)
    anti_CCP_positivity: conint(ge=0, le=1) = Field(...)
    DAS28_ESR: confloat(ge=0) = Field(...)
    patient_global: confloat(ge=0, le=100) = Field(...)
    patient_pain: confloat(ge=0, le=100) = Field(...)
    physician_global: confloat(ge=0, le=100) = Field(...)
    CRP: confloat(ge=0) = Field(...)
    ESR: conint(ge=0) = Field(...)
    SJC28: conint(ge=0, le=28) = Field(...)
    TJC28: conint(ge=0, le=28) = Field(...)

class Treatment(BaseModel):
    concomitant_csDMARDs: conint(ge=0, le=1) = Field(...)
    type_of_concomitant_csDMARD: Optional[conint(ge=1, le=5)] = Field(default=None)
    dose_of_concomitant_csDMARDs: Optional[confloat(ge=0)] = Field(default=None)
    N_previous_csDMARDs: conint(ge=0) = Field(...)

class bDMARDTreatment(BaseModel):
    current_bDMARD_type: conint(ge=1, le=5) = Field(...)
    start_date_current_bDMARD: date = Field(...)
    stop_date_current_bDMARD: Optional[date] = Field(default=None)
    if_stop_reason: Optional[conint(ge=1, le=4)] = Field(default=None)
    
    @validator('stop_date_current_bDMARD', pre=True)
    def stop_date_after_start_date(cls, v, values, **kwargs):
        if 'start_date_current_bDMARD' in values and v is not None:
            if v < values['start_date_current_bDMARD']:
                raise ValueError("stop_date must be after start_date")
        return v

class tsDMARDTreatment(BaseModel):
    current_tsDMARD_type: conint(ge=1, le=4) = Field(...)
    start_date_current_tsDMARD: date = Field(...)
    stop_date_current_tsDMARD: Optional[date] = Field(default=None)
    if_stop_reason: Optional[conint(ge=1, le=4)] = Field(default=None)

    # Similar validator as for bDMARDTreatment can be applied here

class PatientReportedOutcomes(BaseModel):
    EQ5D: Optional[confloat(ge=0)] = Field(default=None)
    HAQ: Optional[confloat(ge=0, le=3)] = Field(default=None)