# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

# Main App
app = FastAPI()

# Code to add middleware - useful for frontend interaction
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = ["http://localhost:3000"],
#     allow_methods = ["*"],
#     allow_headers = ["*"],
# )

# DB connection
redis = get_redis_connection(
    host = "redis-10561.c264.ap-south-1-1.ec2.cloud.redislabs.com",
    port = 10561,
    password = "iyaBMjTd3FfSELLpPx9LmEfkgNDlonVP",
    decode_responses = True
)

# Product Class
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


# GET details of all products
@app.get('/products')
def get_all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


# GET product details based on input pk - primary key
@app.get('/products/{pk}')
def get(pk: str):
        return Product.get(pk)


# POST product into DB
@app.post('/products')
def create(product: Product):
    return product.save()

# DELETE product from DB
@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)