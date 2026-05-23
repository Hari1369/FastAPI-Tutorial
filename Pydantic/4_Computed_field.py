from pydantic import  BaseModel, EmailStr, computed_field
from typing import List, Dict, Tuple
import json



class Patient(BaseModel):
    name            : str
    email           : EmailStr 
    age             : int
    weight          : float
    height          : float
    married         : bool
    allergies       : List[str]
    contact_details : Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight/(self.height**2)
        return bmi



# -----------------------------
# INPUT SECTION
# -----------------------------
name            = input("Enter a Name: ")
email           = input("Enter Email: ")
age             = input("Enter Age: ")
weight          = input("Enter Weight: ")
height          = input("Enter Height: ")
married         = input("Are Your Married: ") or False
allergies       = input("What type of Allergies do You Have: ").split()
phone           = input("Add Contact Number: ")
contact_details = {
    "phone": phone
}


# -----------------------------
# CREATE DICTIONARY
# -----------------------------
patient_data = {
    "name": name,
    "email": email,
    "age": age,
    "weight": weight,
    "height": height,
    "married": married,
    "allergies": allergies,
    "contact_details": contact_details
}

def insert_patient(patient : Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.bmi)
    print("Inserted")

def update_patient(patient : Patient):
    print("Updated")


# -----------------------------
# CONVERT TO JSON
# -----------------------------
patient_data = json.dumps(patient_data, indent=4)
# print(patient_data)
patient_data = json.loads(patient_data)

patient1 = Patient(**patient_data)
insert_patient(patient1)
