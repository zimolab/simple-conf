# Simple Conf

## Basic Usage

```python
import dataclasses
from typing import List
from uuid import uuid4

from simpleconf.config import BaseJsonConfig


@dataclasses.dataclass
class UserProfile(BaseJsonConfig):
    name: str = ""
    uid: int | str = -1
    email: str = ""
    password: str = ""
    is_admin: bool = False
    tags: List[str] = dataclasses.field(default_factory=list)


profile = UserProfile()
profile.name = "Tom"
profile.uid = uuid4().hex
profile.email = "tom@gmail.com"
profile.tags.extend(("Engineer", "Artist"))
# 序列化
serialized = profile.serialize(indent=2)
print(serialized)
# 保存到文件
profile.save("demo_profile.json")

# 反序列化
profile2 = UserProfile.deserialize(serialized)
print(profile2)

# 读取文件
profile3 = UserProfile.load("demo_profile.json")
print(profile3)

assert profile.uid == profile2.uid == profile3.uid
```

## Multiple Formats

```python
import dataclasses
from typing import List

from simpleconf.config import BaseJsonConfig, BaseTomlConfig, BaseYamlConfig


# 使用dataclass定义配置对象结构
# 支持将一个dataclass嵌入到其他dataclass中
# BaseAppConfig
#  - environment
#  - ServerConfig
#  - RuntimeConfig
#  - MySqlConfig
@dataclasses.dataclass
class ServerConfig(object):
    httpPort: int = 8080
    websocketPort: int = 8080
    domain: str = "localhost"
    password: str = ""
    bannedIps: List[str] = dataclasses.field(default_factory=list)
    bannedClientIds: List[str] = dataclasses.field(default_factory=list)
    bannedHostnames: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class RuntimeConfig(object):
    debug: bool = True
    enableLogging: bool = False


@dataclasses.dataclass
class MySqlConfig(object):
    host: str = 'localhost'
    user: str = ''
    password: str = ''
    database: str = ''


@dataclasses.dataclass
class BaseAppConfig(object):
    environment: str = "local"
    server: ServerConfig = ServerConfig()
    mysql: MySqlConfig = MySqlConfig()
    runtime: RuntimeConfig = RuntimeConfig()


# 提供继承
@dataclasses.dataclass
class AppJsonConfig(BaseAppConfig, BaseJsonConfig):
    pass


@dataclasses.dataclass
class AppTomlConfig(BaseAppConfig, BaseTomlConfig):
    pass


@dataclasses.dataclass
class AppYamlConfig(BaseAppConfig, BaseYamlConfig):
    pass


def test_json_config():
    json_conf = AppJsonConfig()
    json_conf.runtime.debug = True
    json_conf.mysql.user = "root"
    json_conf.mysql.password = "password"
    json_conf.mysql.database = "test_db"
    json_conf.server.bannedIps.append("999.999.999.999")
    json_conf.server.bannedClientIds.append("df3453rewr349543utff")
    serialized = json_conf.serialize(indent=2)
    print(serialized)
    json_conf2 = AppJsonConfig.deserialize(serialized)
    print(json_conf2)

    json_conf.save("test.json", indent=4)
    json_conf3 = AppJsonConfig.load("test.json")
    print(json_conf3)


def test_yaml_config():
    yaml_conf = AppYamlConfig()
    yaml_conf.runtime.debug = True
    yaml_conf.mysql.user = "root"
    yaml_conf.mysql.password = "password"
    yaml_conf.mysql.database = "test_db"
    yaml_conf.server.bannedIps.append("999.999.999.999")
    yaml_conf.server.bannedClientIds.append("df3453rewr349543utff")
    print(yaml_conf.serialize())

    yaml_conf2 = AppYamlConfig.deserialize(yaml_conf.serialize())
    print(yaml_conf2)

    yaml_conf2.save("test.yaml", indent=4)
    yaml_conf3 = AppYamlConfig.load("test.yaml")
    print(yaml_conf3)


def test_toml_config():
    toml_conf = AppTomlConfig()
    toml_conf.runtime.debug = True
    toml_conf.mysql.user = "root"
    toml_conf.mysql.password = "password"
    toml_conf.mysql.database = "test_db"
    toml_conf.server.bannedIps.append("999.999.999.999")
    toml_conf.server.bannedClientIds.append("df3453rewr349543utff")
    print(toml_conf.serialize())

    toml_conf2 = AppTomlConfig.deserialize(toml_conf.serialize())
    print(toml_conf2)

    toml_conf2.save("test.toml")
    toml_conf3 = AppTomlConfig.load("test.toml")
    print(toml_conf3)


if __name__ == '__main__':
    test_json_config()
    test_toml_config()
    test_yaml_config()
```

## Field Validation

```python

import dataclasses
from typing import List

import marshmallow.validate
from marshmallow import ValidationError

from simpleconf.config import BaseJsonConfig


@dataclasses.dataclass
class ProjectConfig(BaseJsonConfig):
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


```