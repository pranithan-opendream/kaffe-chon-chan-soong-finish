from app.domain.menu import Menu
from app.domain.menu_repository import IMenuRepository
from .repository import metadata
from sqlalchemy import Column, Integer, Numeric, String, Table, select
from sqlalchemy.orm import Session, composite

menu_table = Table(
    "menu",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('menu_name', String),
    Column('price', Numeric),
    Column('code', String),
    Column('description', String),
)

class MenuRepository(IMenuRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, menu: Menu) -> None:
        self.session.add(menu)

    def find_by_id(self, menu_id) -> Menu:
        return self.session.get(Menu, menu_id)

    def find_by_code(self, code: str) -> Menu:
        return self.session.execute(
            select(Menu)
            .where(menu_table.c.code == code)
        ).scalar_one()
    
    def find_by_menu_name(self, menu_name):
        return self.session.scalars(
            select(Menu)
            .where(menu_table.c.menu_name.like(f"%{menu_name}%"))
            .order_by(menu_table.c.id)
        ).all()

    def find_all(self):
        return self.session.scalars(
            select(Menu)
        ).all()
    
    