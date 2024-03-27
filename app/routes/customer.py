from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends
from app.database import get_db
from app.domain.menu import Menu
from app.infra.menu_repository import MenuRepository
from sqlalchemy.orm import Session

router = APIRouter(prefix="/customer", tags=["customer"])

@dataclass
class MenuDTO:
    id: str
    menu_name: str
    price: Decimal
    code: str
    description: Optional[str] = None

@router.get("/menus/", response_model=list[MenuDTO])
def list_menu(db: Session = Depends(get_db)):
    # TODO: repository injection
    rslt = MenuRepository(db).find_all()
    rslt = [MenuDTO(
        id=str(menu.id),
        menu_name=menu.menu_name,
        price=menu.price,
        code=menu.code,
        description=menu.description,
    ) for menu in rslt]
    return rslt
