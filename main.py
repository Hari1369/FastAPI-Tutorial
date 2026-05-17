from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data

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