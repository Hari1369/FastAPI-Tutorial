
def insert_patient(name:str, age:int):
    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("Age Can't Be Negative")
        else:
            print("inserted")
    else:
        raise TypeError("Incorrect Datatype")


def update_patient(name:str, age:int):
    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("Age Can't Be Negative")
        else:
            print("Updated")
    else:
        raise TypeError("Incorrect Datatype")

name = input("Enter Your Name: ")
age = int(input("Enter Your Age: "))

update_patient(name, age)