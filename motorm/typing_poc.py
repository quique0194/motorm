"""
required
default

precision
choices
max_length

indices
reference
"""
import pprint
import datetime as dt
from decimal import ROUND_HALF_UP
from decimal import Decimal
from decimal import Context
from typing import NamedTuple
from typing import get_type_hints
from dataclasses import dataclass
from dataclasses import is_dataclass
from dataclasses import asdict
from dataclasses import make_dataclass


class Money(Decimal):
    def __new__(cls, value):
        return super().__new__(cls, value, context=Context(prec=2, rounding=ROUND_HALF_UP))


class DecimalField():
    accepted_types = [Decimal, float, str]
    returned_type = Decimal
    def validate(self):
        ...
    def to_mongo(self):
        ...
    def to_python(self):
        ...


# class ReferenceField():
#     accepted_types =


print(Money('10.333333333'))
import sys
sys.exit(0)


class Model:
    REQUIRED = {}

    def __init__(self, **init_params):
        defaults = Model.get_default_values(self.Schema)
        initwdefs = {**init_params, **defaults}
        print('>>>>>> initwdefs', initwdefs)
        for req in self.REQUIRED:
            if req not in initwdefs:
                raise ValueError(f'Missing required param {req}')
        self.orig, errors = Model.dict2ntuple(initwdefs, self.Schema)

    @staticmethod
    def get_default_values(schema):
        fields_with_default = list(filter(lambda s: not s.startswith('__'), dir(schema)))
        dd = {f: getattr(schema, f) for f in fields_with_default}
        return {k: (v() if callable(v) else v) for k, v in dd.items()}

    @classmethod
    def from_dict(cls, d: dict):
        self = cls()
        self.orig, errors = Model.dict2ntuple(d, cls.Schema)
        return self

    @staticmethod
    def dict2ntuple(d: dict, dataclass_type):
        errors = []
        schema = get_type_hints(dataclass_type)
        for k, v in d.items():
            schema_type = getattr(schema[k], '__origin__', schema[k])
            if is_dataclass(schema_type):
                d[k], new_errors = Model.dict2ntuple(d[k], schema_type)
                errors += new_errors
                continue
            if type(v) != schema_type:
                errors.append({k: f'Expected type {schema[k]}, got {type(v)}'})
                continue

            if schema_type == list:
                subtype = schema[k].__args__[0]
                # TODO: process errors returned by Model.dict2ntuple
                d[k] = [Model.dict2ntuple(i, subtype)[0] for i in d[k]]
        theclass = make_dataclass(dataclass_type.__name__, d.keys())
        print(theclass)
        return theclass(**d), errors



class Payment(Model):
    REQUIRED = {'amount'}

    @dataclass(frozen=True)
    class Schema:
        amount: int
        date: dt.date


class Lend(Model):
    REQUIRED = {'amount'}

    @dataclass(frozen=True)
    class Schema:
        amount: DecimalField
        first_name: str
        last_name: str
        score: float
        payments: list[Payment.Schema]
        payment: Payment.Schema
        steps: int = lambda: 0
        approved: bool = False



d = dict(
    amount=100,
    steps=50,
    first_name='jose',
    last_name='carrillo',
    score=3.14,
    # approved=True,
    # payments=[
    #     dict(amount=100, date=dt.date(2022, 11, 15)),
    #     dict(amount=200, date=dt.date(2022, 11, 30)),
    # ],
    # payment=dict(amount=300, date=dt.date(2022, 12, 15)),
)



l = Lend(amount=1000.33333, steps=50)
# l = Lend.from_dict(d)
pprint.pprint(l.orig)
# print(l.payment)
print(asdict(l.orig))