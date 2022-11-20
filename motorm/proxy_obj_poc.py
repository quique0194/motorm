"""
Requisitos:
* Debe funcionar sync y async
* Sólo jalar los campos requeridos con only()
    * Quizá agrupar los campos mediante algún mecanismo
* Manejar la data de forma inmutable
* Los save deben reutilizar el query para evitar race conditions

* Quizá una vez que se hace save, no permitir que se vuelva a editar
* fetch_copy -> Vuelve a hitear la base de datos, con el mismo query que lo creó
* Permitir aggregations
* Easy progressive migration
* Partial document definition


 (1110 + 85 *(2.55)) - (1482 - 95 *(2.55))
"""
from collections import namedtuple
from decimal import Decimal
from typing import NamedTuple
from typing import Any



class Lend:
    class Schema(NamedTuple):
        amount: Decimal
        steps: int

    def __init__(self, *args, **kwargs):
        self.orig = self.Schema(*args, **kwargs)
        self.new = self.orig
        self.changes = {}

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in ['changes', 'orig', 'new']:
            object.__setattr__(self, __name, __value)
            return
        self.new = self.new._replace(**{__name: __value})
        self.changes[__name] = __value

    def __getattribute__(self, __name: str) -> Any:
        if __name in ['Schema', 'changes', 'orig', 'new', 'save']:
            return object.__getattribute__(self, __name)
        print(f'{__name=}')
        return getattr(self.new, __name)

    def save(self):
        print('Storing:', self.changes)

    @classmethod
    def objects(**query) -> 'Queryset':
        pass

    @classmethod
    def objects_async(**query):
        pass

# l = Lend(amount=1000, steps=10)
# print(l.orig)
# l.amount = 2
# p
# rint(l.amount)
# l.steps = 5
# print('orig', l.orig)
# print('changes', l.changes)
# print('upd', l.new)
# l.save()


def ntuple_from_dict(name: str, d: dict):
    MyTuple = namedtuple('MyTuple', d.keys())
    return MyTuple(**d)

print(ntuple_from_dict('Lend', {'a': 1, 'b': 2}))
