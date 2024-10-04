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

