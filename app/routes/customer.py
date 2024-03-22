from fastapi import APIRouter, Depends
from app.database import get_db
from app.domain.menu import Menu
from app.infra.menu_repository import MenuRepository
from sqlalchemy.orm import Session

router = APIRouter(prefix="/customer", tags=["customer"])

@router.get("/menus/", response_model=list[Menu])
def list_menu(db: Session = Depends(get_db)):
    # TODO: repository injection
    rslt = MenuRepository(db).find_all()
    return rslt
