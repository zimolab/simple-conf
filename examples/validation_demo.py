import dataclasses
from typing import List

import marshmallow.validate
from marshmallow import ValidationError

from simpleconf.config import BaseJsonConfig


@dataclasses.dataclass
class ProjectConfig(BaseJsonConfig):
    """Project configuration."""
    name: str
    description: str = "<description>"
    author: str = "<author>"
    author_email: str = "<email>"
    license: str = "MIT"
    version: str = "0.1"
    install_requires: List[str] = dataclasses.field(default_factory=list)


try:
    # 以下代码将引发异常，因为缺少必要字段"name"
    conf = ProjectConfig.deserialize("{}")
except ValidationError as e:
    print(e)

try:
    # 以下代码将引发异常，因为version字段不是字符串
    # 在上面的ProjectConfig类中，version的类型提示为str，若要其同时支持字符串和数字，可以使用 str|int作为其类型提示
    conf2 = ProjectConfig.deserialize(
        """{
        "name": "demo",
        "version": 1
        }"""
    )
except ValidationError as e:
    print(e)

try:
    # 以下代码将引发异常，因为install_requires被定义为List[str]类型，但下面的install_requires中的第一个元素为int类型
    conf3 = ProjectConfig.deserialize(
        """{
        "name": "demo",
        "version": "1.0",
        "install_requires": [1, "toml"]
        }"""
    )
except ValidationError as e:
    print(e)


# 除了类型注释可以为验证器提供足够的信息外，还可以利用dataclass字段的metadata信息为字段提供更加精细的验证器
# 做法是在metadata中添加一个validate属性，该属性的值为marshmallow.validate.Validator类的实例
# 例如在下面的User类中，age字段的metadata中添加了validate属性，其值为marshmallow自带的一个Validator——Range
# 作用是限制age字段的值必须在18~60之间
@dataclasses.dataclass
class User(BaseJsonConfig):
    name: str
    age: int = dataclasses.field(metadata={"validate": marshmallow.validate.Range(min=18, max=60)}, default=18)


try:
    # user1 ok
    user1 = User.deserialize("""{"name": "tom", "age": 18}""")
    # user2 会抛出异常，因为age的值超出了18~60的范围
    user2 = User.deserialize("""{"name": "tom", "age": 100}""")
except ValidationError as e:
    print(e)
