import abc
import dataclasses

import marshmallow_dataclass
from marshmallow import Schema


class Serializable(abc.ABC):
    """"""

    @abc.abstractmethod
    def serialize(self, *args, **kwargs) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, data, *args, **kwargs) -> "Serializable":
        pass

    @abc.abstractmethod
    def as_object(self, *args, **kwargs) -> dict:
        pass

    @classmethod
    @abc.abstractmethod
    def from_object(cls, obj: dict, *args, **kwargs) -> "Serializable":
        pass


@dataclasses.dataclass
class MarshmallowSerializable(Serializable, abc.ABC):
    @classmethod
    def schema(cls) -> Schema:
        _schema = getattr(cls, "__schema__", None)
        if not _schema or not isinstance(_schema, Schema):
            _schema = marshmallow_dataclass.class_schema(cls)()
            setattr(cls, "__schema__", _schema)
            return _schema
        return _schema

    def as_object(self, *args, **kwargs) -> dict:
        return self.schema().dump(self, many=False)

    def serialize(self, *args, **kwargs) -> str:
        obj: dict = self.as_object(*args, **kwargs)
        return self.on_serialize(obj, *args, **kwargs)

    @abc.abstractmethod
    def on_serialize(self, obj: dict, *args, **kwargs) -> str:
        pass

    @classmethod
    def from_object(cls, obj: dict, *args, **kwargs) -> "MarshmallowSerializable":
        return cls.schema().load(obj, many=False, *args, **kwargs)

    @classmethod
    def deserialize(cls, data: str, *args, **kwargs) -> "MarshmallowSerializable":
        obj: dict = cls.on_deserialize(data, *args, **kwargs)
        return cls.from_object(obj, *args, **kwargs)

    @classmethod
    @abc.abstractmethod
    def on_deserialize(cls, data: str, *args, **kwargs) -> dict:
        pass

    def save(self, filepath: str, encoding: str = "utf-8", *args, **kwargs):
        with open(filepath, "w", encoding=encoding) as f:
            f.write(self.serialize(*args, **kwargs))

    @classmethod
    def load(cls, filepath: str, encoding: str = "utf-8", *args, **kwargs) -> "MarshmallowSerializable":
        with open(filepath, "r", encoding=encoding) as f:
            return cls.deserialize(f.read(), *args, **kwargs)
