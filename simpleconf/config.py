import dataclasses
import json

import tomli
import tomli_w
import yaml

from simpleconf.base import MarshmallowSerializable


@dataclasses.dataclass
class BaseJsonConfig(MarshmallowSerializable):
    """
    基于Json格式的配置对象
    """

    def on_serialize(self, obj: dict, ensure_ascii: bool = False, indent: int | None = 4, **kwargs) -> str:
        """将字典序列化为json字符串"""
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, **kwargs)

    @classmethod
    def on_deserialize(cls, data: str, *args, **kwargs) -> dict:
        """将json字符串反序列化为字典"""
        return json.loads(data, *args, **kwargs)

    def save(self, filepath: str, encoding: str = "utf-8", ensure_ascii: bool = False, indent: int | None = 4,
             **kwargs):
        super().save(filepath, encoding, ensure_ascii=ensure_ascii, indent=indent, **kwargs)


@dataclasses.dataclass
class BaseTomlConfig(MarshmallowSerializable):
    """
    基于Toml格式的配置对象。限制：Toml标准不支持None（null）类型数据，在配置项中使用None可能会引发异常，或造成难以察觉的逻辑错误。

    序列化和反序列化功能由toml库提供。
    """

    def on_serialize(self, obj: dict, *args, **kwargs) -> str:
        """将字典序列化为toml字符串"""
        return tomli_w.dumps(obj, *args, **kwargs)

    @classmethod
    def on_deserialize(cls, data: str, *args, **kwargs) -> dict:
        """将toml字符串反序列化为字典"""
        return tomli.loads(data, *args, **kwargs)


@dataclasses.dataclass
class BaseYamlConfig(MarshmallowSerializable):
    """
    基于Yaml格式的配置对象。

    使用pyyaml库实现序列化和反序列化功能。
    """

    def on_serialize(self, obj: dict, *args, **kwargs) -> str:
        """将字典序列化为yaml字符串"""
        return yaml.dump(obj, stream=None, *args, **kwargs)

    @classmethod
    def on_deserialize(cls, data: str, Loader=yaml.FullLoader, **kwargs) -> dict:
        """将yaml字符串反序列化为字典"""
        obj = yaml.load(data, Loader=Loader)
        if not isinstance(obj, dict):
            raise RuntimeError("Yaml data must be a dict")
        return obj
