from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends
from starlette.responses import Response
from app.database import get_db
from app.domain.menu import Menu
from app.infra.menu_repository import MenuRepository
from sqlalchemy.orm import Session

from app.shared import get_id

router = APIRouter(prefix="/cashier", tags=["cashier"])

@dataclass
class EditMenuDTO:
    menu_name: str
    price: Decimal
    code: str
    description: Optional[str] = None

@dataclass
class MenuDTO:
    id: str
    menu_name: str
    price: Decimal
    code: str
    description: Optional[str] = None

@router.post("/menus/")
def add_menu(new_menu: EditMenuDTO, db: Session = Depends(get_db)) -> "MenuDTO":
    # TODO: repository injection
    menu = Menu(
        get_id(),
        menu_name=new_menu.menu_name,
        price=new_menu.price,
        code=new_menu.code,
        description=new_menu.description,
    )
    MenuRepository(db).save(menu)
    db.commit()
    new_menu = MenuDTO(
        id=str(menu.id),
        menu_name=menu.menu_name,
        price=menu.price,
        code=menu.code,
        description=menu.description,
    )
    return new_menu

@router.put("/menus/{id}")
def update_menu(id: str, updated_menu: EditMenuDTO, db: Session = Depends(get_db)) -> "MenuDTO":
    menu = MenuRepository(db).find_by_id(int(id))
    menu.menu_name = updated_menu.menu_name
    menu.price = updated_menu.price
    menu.code = updated_menu.code
    menu.description = updated_menu.description
    MenuRepository(db).save(menu)
    db.commit()
    updated_menu = MenuDTO(
        id=str(menu.id),
        menu_name=menu.menu_name,
        price=menu.price,
        code=menu.code,
        description=menu.description,
    )
    return updated_menu

@router.get("/menus/{id}")
def get_menu(id: str, db: Session = Depends(get_db)) -> MenuDTO:
    menu = MenuRepository(db).find_by_id(int(id))
    menu = MenuDTO(
        id=str(menu.id),
        menu_name=menu.menu_name,
        price=menu.price,
        code=menu.code,
        description=menu.description,
    )
    return menu

# TODO: Router get by code
# TODO: Router get by name