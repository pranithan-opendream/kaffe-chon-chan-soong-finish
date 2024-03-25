
from abc import ABC, abstractmethod
from typing import Any

def _inject__eq__(cls, iden_field_name):
    def __eq__(self, __value) -> bool:
        if not isinstance(__value, cls):
            return False
        if iden_field_name not in self.__dict__ or iden_field_name not in __value.__dict__:
            return False
        return getattr(self, iden_field_name) == getattr(__value, iden_field_name)
    cls.__eq__ = __eq__
    return cls

# This code mimic the behavior of @dataclass

# in case of @entity the call sequence is:
# entity(A) -> wrap(A)

# in case of @entity(iden_field_name="id") the call sequence is:
# entity(iden_field_name="id") -> wrap(B)

def entity(cls=None, *, iden_field_name: str = "id"):
    def wrap(cls):
        return _inject__eq__(cls, iden_field_name)
    
    if cls is None:
        return wrap
    
    return wrap(cls)
