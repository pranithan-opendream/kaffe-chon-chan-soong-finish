
from dataclasses import dataclass
from app.domain.entity import entity

@entity
@dataclass
class A:
    id: int
    another_val: str

@entity(iden_field_name="id")
@dataclass
class B:
    id: int
    another_val: str

def test_eq_same_instance_a():
    instance1 = A(1, "abc")
    instance2 = A(1, "bcd")
    assert instance1 == instance2

def test_eq_same_instance_b():
    instance1 = B(1, "abc")
    instance2 = B(1, "bcd")
    assert instance1 == instance2