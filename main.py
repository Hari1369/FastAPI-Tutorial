from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, computed_field, Field
from typing import List, Dict, Tuple, Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id      : Annotated[str, Field(..., description="ID of the Patient", example="P001")] 
    name    : Annotated[str, Field(..., description="Name of the Patient")]
    city    : Annotated[str, Field(..., description="Enter City Name")]
    age     : Annotated[int, Field(..., gt=0, lt=75)]
    gender  : Annotated[Literal['Male','Female','Other'], Field(..., description="Gender of the Patient")]
    height  : Annotated[float, Field(..., gt=0, description="Enter Height of the Patient")]
    weight  : Annotated[float, Field(..., gt=0, description="Enter Weight of the Patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Under Weight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'


class Patient_Update(BaseModel):
    name : Annotated[Optional[str], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None, gt=0)]
    gender : Annotated[Optional[Literal['male','female','other']], Field(default=None)]
    height : Annotated[Optional[float], Field(default=None, gt=0)]
    weight : Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return{'message':'Patient Manage with System API'}

@app.get('/about')
def about():
    return{'message': 'Fully functional API to Manage your Patient records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
# ===============================================================================================> SPECIFIC DESCRIPTION
# def view_patient(patient_id: str = Path(..., description = "ID of the Patient in the DB", example = "P001", )):
# ===============================================================================================> SPECIFIC DESCRIPTION
def view_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        # return {'error': "Patient Not Found "}
        raise HTTPException(status_code=404, detail = "Patient Not Found")


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description = "Sort on the Basis of Height, Weight or bmi"), order : str = Query('asc', description = "Sort in Ascending and Descending")):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail = 'Invalid Field Select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order selection between Ascending and descending")

    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post('/create_patient')
def create_patien(patient: Patient):
    # LOAD EXISTING DATA
    data = load_data()

    # CHECK IF PATIENT IS ALREADY EXIST OR NOT
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist!")

    # EXCLUDEING THE ID
    data[patient.id] = patient.model_dump(exclude=['id'])

    # SAVE INTO JSON FILE
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'Patient Created Successfully'})

# ==================================================>
# Load JSON
#    ↓
# Get Existing Patient
#    ↓
# Get Only Updated Fields
#    ↓
# Merge Updated Fields Into Existing Data
#    ↓
# Convert To Pydantic Object
#    ↓
# Recalculate BMI + Verdict
#    ↓
# Convert Back To Dictionary
#    ↓
# Store In Main Data
#    ↓
# Save JSON File
# ==================================================>
@app.put('/update/{patient_id}')
def update_patient(patient_id : str, patient_update : Patient_Update):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")

    existing_patient_info = data[patient_id]

    # update_patient_info --> dictionary
    update_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in update_patient_info.items():
        existing_patient_info[key] = value

    # existing patient info -> pydantic obj -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    # pydantic object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')
    
    data[patient_id] = existing_patient_info
    save_data(data)
    return JSONResponse(status_code=200, content={'message':"Patiend Updated Successfull"})




@app.get('/delete/{patiend_id}')
def delete_delete(patiend_id: str):
    data = load_data()

    if patiend_id not in data:
        raise HTTPException(status_code=404, detail="Patiend Not Found")

        del data[patiend_id]

        save_data(data)

        return JSONResponse(status_code=200, content={'message':'patient deleted'}) 