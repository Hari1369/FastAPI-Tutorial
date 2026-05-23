from pydantic import BaseModel, AnyUrl, Field, EmailStr, field_validator
from typing import List, Dict
import json

class Patient(BaseModel):
    name            : str = Field(max_length = 50)
    email           : EmailStr
    linked_url      : AnyUrl
    age             : int = Field(gt = 0)
    married         : bool = False
    allergies       : List[str]
    contact_details : Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ["hdfc.com","icici.com"]
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError("Not a Valid domain")
        else:
            return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()


def insert_patient(patient : Patient):
    print("Inserted")

def update_patient(patient : Patient):
    print("Updated")

# -----------------------------
# INPUT SECTION
# -----------------------------
name            = input("Enter a Name: ")
email           = input("Enter Email: ")
age             = input("Enter Age: ") 
married         = input("Are Your Married: ") or False
linked_url      = input("Enter Linked Url: ")
allergies       = input("What type of Allergies do You Have: ").split()
contact_details = {
    "phone": input("Add Contact Details: ")
}

# -----------------------------
# CREATE DICTIONARY
# -----------------------------
patient_data = {
    "name": name,
    "email": email,
    "age": age,
    "married": married,
    "linked_url": linked_url,
    "allergies": allergies,
    "contact_details": contact_details
}

# -----------------------------
# CONVERT TO JSON
# -----------------------------
patient_data = json.dumps(patient_data, indent=4)
print(patient_data)
patient_data = json.loads(patient_data)

patient1 = Patient(**patient_data)
update_patient(patient1)