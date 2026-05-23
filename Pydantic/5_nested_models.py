from pydantic import BaseModel


class Address(BaseModel):
    city : str
    state : str
    pin : str

class Patient(BaseModel):
    name : str
    gender : str
    age : int
    address : Address


city    = input("Enter City: ")
state   = input("Enter State: ")
pin     = input("Enter Pin: ")


address_dict = {
    "city": city,
    "state": state,
    "pin": pin
}

address1 = Address(**address_dict)

name    = input("Enter Name: ")
age  = input("Enter age: ")
gender  = input("Enter Gender: ")

patient_dict = {
    "name"      : name,
    "gender"    : gender,
    "age"       : age,
    "address"   : address1
}

patient1 = Patient(**patient_dict)

print(patient1)
