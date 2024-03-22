from dataclasses import dataclass
from decimal import Decimal
from fastapi import APIRouter, Depends
from starlette.responses import Response
from app.database import get_db
from app.domain.menu import Menu
from app.infra.menu_repository import MenuRepository
from sqlalchemy.orm import Session

from app.shared import get_id

router = APIRouter(prefix="/cashier", tags=["cashier"])

@dataclass
class MenuDTO:
    menu_name: str
    price: Decimal
    code: str

@router.post("/menus/", response_model=Menu)
def add_menu(new_menu: MenuDTO, db: Session = Depends(get_db)):
    # TODO: repository injection
    menu = Menu(get_id(), menu_name=new_menu.menu_name, price=new_menu.price, code=new_menu.code)
    MenuRepository(db).save(menu)
    db.commit()
    return menu

@router.put("/menus/{id}", response_model=Menu)
def update_menu(id: int, updated_menu: MenuDTO, db: Session = Depends(get_db)):
    menu = MenuRepository(db).find_by_id(id)
    menu.menu_name = updated_menu.menu_name
    menu.price = updated_menu.price
    menu.code = updated_menu.code
    MenuRepository(db).save(menu)
    db.commit()
    return menu