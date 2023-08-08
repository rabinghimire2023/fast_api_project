from fastapi import FastAPI, HTTPException
from app.models import Employee
from app.database import con, cur

app=FastAPI()

@app.on_event("startup")
async def startup():
    """
    Function to set up the database connection and enable foreign keys on startup.
    """
    con.execute("PRAGMA foreign_keys = ON;")
    con.commit()
    
@app.get("/employees")
def get_employees():
    """
    Retrieve a list of all employees from the database.

    Returns:
        List[Employee]: A list of Employee objects representing employees.
    """
    cur.execute("SELECT * FROM Employees")
    employees = cur.fetchall()
    return employees

@app.get("/employees/{employee_id}")
def get_employee(employee_id:int):
    """
    Retrieve an employee by their ID from the database.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        Employee: An Employee object representing the employee.

    Raises:
        HTTPException: If the employee with the specified ID is not found.
    """
    cur.execute("SELECT * FROM Employees WHERE id=?",(employee_id,))
    employee = cur.fetchone()
    if employee is None:
        raise HTTPException(status_code = 404,details="Employee not found")
    return employee

@app.post("/employees/")
def create_employee(employee:Employee):
    """
    Create a new employee and insert them into the database.

    Args:
        employee (Employee): The Employee object representing the new employee.

    Returns:
        dict: A dictionary with a message confirming the employee creation.
    """
    cur.execute("INSERT INTO Employees (name,department) VALUES (?,?)",(employee.name,employee.department))
    con.commit()
    return {"message":"Employee added"}
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    """
    Delete an employee from the database by their ID.

    Args:
        employee_id (int): The ID of the employee to be deleted.

    Returns:
        dict: A dictionary with a message confirming the employee deletion.
    """
    cur.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    con.commit()
    return {"message": "Employee deleted"}

@app.put("/employees/{employee_id}/{column}/{new_value}")
def update_employee(employee_id:int,column:str,new_value:str):
    """
    Update a specific attribute of an employee in the database.

    Args:
        employee_id (int): The ID of the employee to be updated.
        column (str): The name of the column to be updated (name or department).
        new_value (str): The new value to be set for the specified column.

    Returns:
        dict: A dictionary with a message confirming the employee attribute update.

    Raises:
        HTTPException: If an invalid column name is provided.uvicorn app.main:app --host localhost --port 8000 --reload

    """
    valid_columns = ["name","department"]
    if column not in valid_columns:
        raise HTTPException(status_code=400,details="Invalid columns name")
    
    cur.execute(f"UPDATE Employees SET {column}=? WHERE id=?",(new_value,employee_id))
    con.commit()
    return {"message":f"Employee{column} updated"}

    