from __future__ import annotations
from dataclasses import dataclass
import base64
from datetime import datetime
from typing import Optional

@dataclass
class DiscordUser:
    id: int
    epoch: int = 1420070400000
    # Token 
    first, second, third = (None, None, None)

    # gen you can change everything into not a property i sleep

    @classmethod
    def from_token(cls, token: str) -> DiscordUser:
        first, second, third = token.split(".")
        try:
            id = int(base64.b64decode(first))
        except:
            id = int(base64.b64decode(first + "=="))
        user = DiscordUser(id)
        user.first = first
        user.second = second
        user.third = third
        return user



    @property
    def base64_token(self) -> str:
        return base64.b64encode(bytes(self.id)).decode().removesuffix("==")

    @property
    def creation_timestamp(self) -> float:
        ms = (self.id >> 22) + self.epoch
        return ms / 1000


    @property
    def creation_date(self):
        """The creation_date property."""
        return datetime.fromtimestamp(self.creation_timestamp)

    @creation_date.setter
    def creation_date(self, value):
        self._creation_date = value

    @property
    def id_bytes(self) -> str:
        return bin(self.id)[2:]

    @property
    def worker_id(self) -> int:
        return (self.id >> 17) & 0x1F

    @property
    def process_id(self) -> int:
        return (self.id >> 12) & 0x1F 

    @property
    def increment(self) -> int:
        return self.id & 0xFFF 
