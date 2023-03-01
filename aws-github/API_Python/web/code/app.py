from fastapi import FastAPI ,Response ,status
import sqlalchemy
import os
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
baseUrl="/api/v1/employees"



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dbuser=os.getenv("MARIADB_USER")
dbpass=os.getenv("MARIADB_PASSWORD")
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://" + dbuser + ":" + dbpass +"@bdd:3306/employee")
Base = declarative_base()


class Employeedb(Base):
    __tablename__ = 'employees'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    firstName = sqlalchemy.Column(sqlalchemy.String(length=100))
    lastName = sqlalchemy.Column(sqlalchemy.String(length=100))
    emailId = sqlalchemy.Column(sqlalchemy.String(length=100))


class EmployeeBody(BaseModel):
    id: int | None = None
    firstName: str | None = None
    lastName: str | None = None
    emailId: str | None = None


Base.metadata.create_all(engine)

session = sqlalchemy.orm.sessionmaker()
session.configure(bind=engine)
session = session()






@app.get(baseUrl, status_code=200)
def get_employees(response: Response):
    session.commit()
    employees = None
    employees = session.query(Employeedb).all()
    if len(employees) == 0:
       message=  "no employees found in db "
    else:
        message = employees
    return message

@app.get("/api/v1/employees/{EmployeeId}")
def view_employee(EmployeeId: int , response: Response):
    session.commit()
    employeeToFetch= session.get(Employeedb, EmployeeId)
    if employeeToFetch is None:
        message = "employee not found"
        response.status_code=status.HTTP_404_NOT_FOUND
    else: message = employeeToFetch
    return message


@app.post(baseUrl, status_code=201)
def create_item(employee: EmployeeBody , response: Response):
    try:
        newEmployee = Employeedb(firstName=employee.firstName,
                             lastName=employee.lastName, emailId=employee.emailId)
        session.add(newEmployee)
        session.commit()
        message= "Employee  Created"
    except:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        message="an error was encountered"



    return {"message": message}


@app.delete("/api/v1/employees/{EmployeeId}" , status_code=200)
def delete_item(EmployeeId: int , response: Response):
    employeeToDelete = session.get(Employeedb, EmployeeId)
    if employeeToDelete is None:
        message = "employee not found"
        response.status_code=status.HTTP_404_NOT_FOUND

    else:
        try:
            session.delete(employeeToDelete)
            session.commit()
            message = "employee deleted "
        except:
            message= "an error occured"
            response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR

#    session.commit()
    return {"message": message}


@app.put("/api/v1/employees/{EmployeeId}" , status_code=200)
def update_item(EmployeeId: int, updatedinfo: EmployeeBody , response : Response):
    employeeToUpdate  = session.get(Employeedb, EmployeeId)
    if employeeToUpdate is None:
        message = "employee not found"
        response.status_code=status.HTTP_404_NOT_FOUND

    else:
        try:
            if updatedinfo.emailId is not None:
                employeeToUpdate.emailId=updatedinfo.emailId
            if updatedinfo.firstName is not None:
                employeeToUpdate.firstName=updatedinfo.firstName
            if updatedinfo.lastName is not None:
                employeeToUpdate.lastName=updatedinfo.lastName
            session.commit()
            message=session.get(Employeedb, EmployeeId)
        except:
            message= "an error occured"
            response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR

    return  message
