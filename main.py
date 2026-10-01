from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import Product
from schemas import ProductCreate, ProductResponse


app = FastAPI()


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greet():
    return "Hello, welcome to the program!"


@app.get("/products", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):

    return db.query(Product).all()


@app.get("/products/{id}", response_model=ProductResponse)
def get_one_product(
    id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        return {"error": "Product not found"}

    return product


@app.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.put("/products/{id}", response_model=ProductResponse)
def update_product(
    id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        return {"error": "Product not found"}

    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.quantity = updated_product.quantity

    db.commit()
    db.refresh(product)

    return product


@app.delete("/products/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        return {"error": "Product not found"}

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}