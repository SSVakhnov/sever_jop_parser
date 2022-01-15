"""
Этот докцумент описывает кснтанты выбора в приложении
"""
from enum import Enum

__all__ = [
    'BaseType', 'CategoryType', 'PositionType', 'ParseLink'
]


class BaseType(Enum):
    """ Хранит набор метдов для объявления кастомных перечислений в приложении """

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def named_choices(cls):
        return [(key.name, key.value) for key in cls]

    @classmethod
    def values(cls):
        return [key.value for key in cls]

    @classmethod
    def names(cls):
        return [key.name for key in cls]

    @classmethod
    def value_by_names(cls, t_name):
        return cls.__getattr__(t_name).value


class CategoryType(BaseType):
    PYTHON = 'python'
    DOT_NET = '.net'


class PositionType(BaseType):
    INTERN = 'intern'
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'
    TEAM_LEAD = 'team lead'


class ParseLink(BaseType):
    DOU = 'https://jobs.dou.ua/vacancies/'
