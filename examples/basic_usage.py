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