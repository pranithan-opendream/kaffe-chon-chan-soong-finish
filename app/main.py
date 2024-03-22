from fastapi import Depends, FastAPI, HTTPException

from .database import SessionLocal, engine
from .routes.customer import router as customer_router
from .routes.cashier import router as cashier_router


app = FastAPI()


app.include_router(customer_router)

app.include_router(cashier_router)