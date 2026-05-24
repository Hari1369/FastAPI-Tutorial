from pydantic import BaseModel, AnyUrl, EmailStr, model_validator
from typing import List, Dict
import json


class Patient(BaseModel):
    name            : str
    email           : EmailStr 
    age             : int
    weight          : float
    married         : bool 
    allergies       : List[str] 
    contact_details : Dict[str, str]

    @model_validator(mode="after")
    def validate_emergency_patient(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older then 60 must have emergency contact')
        return model



# -----------------------------
# INPUT SECTION
# -----------------------------
name            = input("Enter a Name: ")
email           = input("Enter Email: ")
age             = input("Enter Age: ")
weight          = input("Enter Weight: ")
married         = input("Are Your Married: ") or False
allergies       = input("What type of Allergies do You Have: ").split()
phone           = input("Add Contact Number: ")
emergency       = input("Add Emergency Contact (Press Enter to Skip): ")

contact_details = {
    "phone": phone
}

if emergency:
    contact_details["emergency"] = emergency


# -----------------------------
# CREATE DICTIONARY
# -----------------------------
patient_data = {
    "name": name,
    "email": email,
    "age": age,
    "weight": weight,
    "married": married,
    "allergies": allergies,
    "contact_details": contact_details
}

def insert_patient(patient : Patient):
    print("Inserted")

def update_patient(patient : Patient):
    print("Updated")


# -----------------------------
# CONVERT TO JSON
# -----------------------------
patient_data = json.dumps(patient_data, indent=4)
print(patient_data)
patient_data = json.loads(patient_data)

patient1 = Patient(**patient_data)
update_patient(patient1)
