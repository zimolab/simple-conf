import dataclasses
from abc import ABC
from collections import OrderedDict
from typing import List, Dict, TypeAlias

from simpleconf import MarshmallowSerializable, BaseTomlConfig

BasicDataType: TypeAlias = str | int | bool | float | list | tuple | dict


@dataclasses.dataclass
class CellRule(object):
    fn: str
    args: List[BasicDataType] = dataclasses.field(default_factory=list)
    kwargs: dict[str, BasicDataType] = dataclasses.field(default_factory=dict)
    per_cell: bool = True


@dataclasses.dataclass
class CellRulesConfig(MarshmallowSerializable, ABC):
    version: int | str = 1
    globals: Dict[str, BasicDataType] = dataclasses.field(default_factory=dict)
    rules: Dict[str, List[CellRule]] = dataclasses.field(default_factory=OrderedDict)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)


@dataclasses.dataclass
class TomlCellRulesConfig(CellRulesConfig, BaseTomlConfig):
    pass

if __name__ == '__main__':
    conf = TomlCellRulesConfig.create(
        version="1.0",
        globals={"a": 1, "b": 2},
        rules={
            "a": [
                CellRule(fn="add", args=[1, 2], kwargs={"c": 3}, per_cell=False),
                CellRule(fn="add", args=[1, 2], kwargs={"c": 3}, per_cell=True),
            ],
            "b": [
                CellRule(fn="add", args=[1, 2], kwargs={"c": 3}, per_cell=True),
            ]
        }
    )
    conf.save("a.toml")
    conf2 = TomlCellRulesConfig.load("a.toml")
    print(conf2)

    conf3 = TomlCellRulesConfig.load("b.toml")
    print(conf3)
