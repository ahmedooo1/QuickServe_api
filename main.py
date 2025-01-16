from fastapi import FastAPI
from interfaces.api import router as user_router
from interfaces.order_api import router as order_router
from infrastructure.db import create_user_database, create_order_database

app = FastAPI()

create_user_database()
create_order_database()

# Register routers
app.include_router(user_router, prefix="/api")
app.include_router(order_router, prefix="/api")
