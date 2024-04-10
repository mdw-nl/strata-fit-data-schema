from datetime import date
from typing import Optional
from pydantic import BaseModel, validator, constr, conint, confloat

class Patient(BaseModel):
    date_of_visit: date
    date_of_birth: date
    sex: conint(ge=0, le=1)
    date_of_RA_diagnosis: date
    
    @validator('date_of_birth', 'date_of_RA_diagnosis')
    def date_not_in_future(cls, v, field, values, **kwargs):
        if v > date.today():
            raise ValueError(f"{field.name} must not be in the future")
        return v

class ClinicalAssessment(BaseModel):
    RF_positivity: conint(ge=0, le=1)
    anti_CCP_positivity: conint(ge=0, le=1)
    DAS28_ESR: confloat(ge=0)
    patient_global: conint(ge=0, le=100)
    patient_pain: conint(ge=0, le=100)
    physician_global: conint(ge=0, le=100)
    CRP: confloat(ge=0)  # Assuming no upper bound specified
    ESR: conint(ge=0)  # Assuming no upper bound specified
    SJC28: conint(ge=0, le=28)
    TJC28: conint(ge=0, le=28)

class Treatment(BaseModel):
    concomitant_csDMARDs: conint(ge=0, le=1)
    type_of_concomitant_csDMARD: Optional[conint(ge=1, le=5)]
    dose_of_concomitant_csDMARDs: Optional[confloat(ge=0)]
    N_previous_csDMARDs: conint(ge=0)

class bDMARDTreatment(BaseModel):
    current_bDMARD_type: conint(ge=1, le=5)
    start_date_current_bDMARD: date
    stop_date_current_bDMARD: Optional[date]
    if_stop_reason: Optional[conint(ge=1, le=4)]

    @validator('stop_date_current_bDMARD')
    def stop_date_after_start_date(cls, v, values, **kwargs):
        if 'start_date_current_bDMARD' in values and v is not None:
            if v < values['start_date_current_bDMARD']:
                raise ValueError("stop_date must be after start_date")
        return v

class tsDMARDTreatment(BaseModel):
    current_tsDMARD_type: conint(ge=1, le=4)
    start_date_current_tsDMARD: date
    stop_date_current_tsDMARD: Optional[date]
    if_stop_reason: Optional[conint(ge=1, le=4)]

    @validator('stop_date_current_tsDMARD')
    def stop_date_after_start_date(cls, v, values, **kwargs):
        if 'start_date_current_tsDMARD' in values and v is not None:
            if v < values['start_date_current_tsDMARD']:
                raise ValueError("stop_date must be after start_date")
        return v

class PatientReportedOutcomes(BaseModel):
    EQ5D: Optional[confloat(ge=0)]  # Assuming no upper bound specified
    HAQ: Optional[confloat(ge=0, le=3)]

# Example usage
if __name__ == "__main__":
    patient_example = Patient(
        date_of_visit=date(2022, 9, 12),
        date_of_birth=date(1980, 6, 15),
        sex=1,
        date_of_RA_diagnosis=date(2019, 3, 10)
    )
    print(patient_example)
