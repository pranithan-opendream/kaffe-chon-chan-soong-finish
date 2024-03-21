from app.domain.menu import Menu
from app.infra.repository import mapper_registry
from .menu_repository import menu_table

def init_mapper():
    mapper_registry.map_imperatively(
        Menu,
        menu_table,
    )
