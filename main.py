from fastapi import FastAPI, status, HTTPException
import schemas
from typing import Optional
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from passlib.context import CryptContext

app = FastAPI()

# Creates all tables defined in models module
models.Base.metadata.create_all(bind=engine)

# Get all customers
@app.get("/customers")
async def get_customer(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return customers

# Get customer by id
@app.get("/customers/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowCustomer)
async def get_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.CustomerID == id
    ).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer ID: {id} has not found.")
    return customer

# Create a customer
@app.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(request: schemas.Customer, db: Session = Depends(get_db)):
    new_customer = models.Customer(Gender = request.Gender,
                                   Age = request.Age,
                                   AnnualIncome = request.AnnualIncome,
                                   SpendingScore = request.SpendingScore)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# Delete a customer by id
@app.delete("/customers/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.CustomerID == id
    ).delete(synchronize_session=False)

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer ID: {id} has not found.")

    db.commit()

    return {"detail": f"Customer {id} deleted.."}

# Update a customer
@app.put("/customers/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_customer_by_id(id: int, request: schemas.Customer, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.CustomerID == id
    )

    if not customer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer ID: {id} has not found")

    customer.update(request.dict(), synchronize_session=False)
    db.commit()
    return {"detail": f"Customer {id} updated."}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)


# Create User
@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.Showuser)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name = request.name,
        email = request.email,
        password = get_password_hash(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user