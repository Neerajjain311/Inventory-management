# Imports
import time
from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests

# Main App
app = FastAPI()

# Middleware code for frontend interaction
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = ["http://localhost:3000"],
#     allow_methods = ["*"],
#     allow_headers = ["*"],
# )

# DB Connection
redis = get_redis_connection(
    host = "redis-10561.c264.ap-south-1-1.ec2.cloud.redislabs.com",
    port = 10561,
    password = "iyaBMjTd3FfSELLpPx9LmEfkgNDlonVP",
    decode_responses = True
)

# Class Order
class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str # pending, completed, refunded

    class Meta:
        database = redis


# GET specific order details
@app.get("/orders/{pk}")
def get_order(pk: str):
    order = Order.get(pk)
    redis.xadd('refund_order', order.json(), '*')
    return order


#POST new order
@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks): # id, quantity
    body = await request.json()

    req = requests.get("http://localhost:8000/products/%s" %body['id'])
    product = req.json()

    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.25 * product['price'],
        total = 1.25 * product['price'],
        quantity = body['quantity'],
        status = 'pending'
    )

    order.save()

    # adding background_tasks
    background_tasks.add_task(order_completed, order)
    return order

# Order execution delayed by 5s to mimic real time scenario
def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')