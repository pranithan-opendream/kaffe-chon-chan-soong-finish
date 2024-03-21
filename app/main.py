from fastapi import Depends, FastAPI, HTTPException

from .database import SessionLocal, engine
from .routes.customer import router as customer_router


app = FastAPI()


app.include_router(customer_router)