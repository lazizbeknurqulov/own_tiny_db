"""
Utility functions
"""

from collections import OrderedDict, abc
from typing import List, Iterator, TypeVar, Generic, Union, Optional, Type, TYPE_CHECKING

K = TypeVar('K')
V = TypeVar('V')
D = TypeVar('D')
T = TypeVar('T')

__all__ = ('LRUCache', "freeze", "with_typehint")


def with_typehint(baseclass: Type[T]):
    """
        Add type hints from a specified class to a base class:

        >>> class Foo(with_typehint(Bar)):
        ...     pass

        This would add type hints from class ``Bar`` to class ``Foo``.

        Note that while PyCharm and Pyright (for VS Code) understand this pattern,
        MyPy does not. For that reason TinyDB has a MyPy plugin in
        ``mypy_plugin.py`` that adds support for this pattern.
        """

    if TYPE_CHECKING:
        return baseclass

    return object


class LRUCache(abc.MutableMapping, Generic[K, V]):

    def __init__(self, capacity=None)->None:
        self.capacity = capacity
        self.cache: OrderedDict[K, V] = OrderedDict()

    @property
    def lru(self) -> List[K]:
        return list(self.cache)

    @property
    def length(self)-> int:
        return len(self.cache)

    def clear(self) -> None:
        self.cache.clear()

    def __len__(self) -> int:
        return self.length

    def __contains__(self, item: object) -> bool:
        return key in self.cache

    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)

    def __delitem__(self, key: K)-> None:
        del self.cache[key]

    def __getitem__(self, key) -> V:
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __iter__(self) -> Iterator[k]:
        return iter(self.cache)

    def get(self, key: K, default: Optional[D]=None) -> Optional[Union[V, D]]:
        value = self.cache.get(key)
        if value is not None:
            self.cache.move_to_end(key, last=True)
            return value
        return default


    def set(self, key: K, value: V):
        if self.cache.get(key):
            self.cache.move_to_end(key, last=True)

        else:
            self.cache[key] = value
            if self.capacity is not None and self.length > self.capacity:
                self.cache.popitem(last=False)



