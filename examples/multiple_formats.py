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
