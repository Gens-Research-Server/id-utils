from __future__ import annotations
import base64
from datetime import datetime
from typing import Optional


class DiscordUser:
    def __init__(self, id: int, first: Optional[str] = None, second: Optional[str] = None, third: Optional[str] = None) -> None:
        self.id: int = id
        self.epoch: int = 1420070400000
        self.new_epoch: int = 1640995200000
        self.first: Optional[str] = first
        self.second: Optional[str] = second
        self.third: Optional[str] = third

        self.creation_timestamp: float = ((self.id >> 22) + self.epoch) / 1000
        self.creation_date: datetime = datetime.fromtimestamp(self.creation_timestamp)
        self.id_bytes: str = bin(self.id)[2:]
        self.worker_id: int = (self.id >> 17) & 0x1F
        self.process_id: int = (self.id >> 12) & 0x1F
        self.increment: int = self.id & 0xFFF

        self.second_timestamp: Optional[float] = self._decode_second_to_timestamp()
        self.second_date: Optional[datetime] = (
            datetime.fromtimestamp(self.second_timestamp) if self.second_timestamp else None
        )

        self.new_second_timestamp: Optional[float] = self._decode_new_second_to_timestamp()
        self.new_second_date: Optional[datetime] = (
            datetime.fromtimestamp(self.new_second_timestamp) if self.new_second_timestamp else None
        )

    @classmethod
    def from_token(cls, token: str) -> DiscordUser:
        first, second, third = token.split(".")
        id = int(base64.b64decode(first + "=="))
        return DiscordUser(id, first, second, third)

    @property
    def base64_token(self) -> str:
        """Generates a Base64 token from the user's ID."""
        return base64.b64encode(str(self.id).encode()).decode().removesuffix("==")

    def _decode_second_to_timestamp(self) -> Optional[float]:
        """Helper function to decode the second part of the token."""
        if not self.second:
            return None
        try:
            decoded = base64.b64decode(self.second)
            return int.from_bytes(decoded, byteorder="big")
        except Exception as e:
            decoded = base64.b64decode(self.second + "==")
            return int.from_bytes(decoded, byteorder="big")

    def _decode_new_second_to_timestamp(self) -> Optional[float]:
        """
        Helper function to decode the second part of the token. 
        Doesn't yet work as this is intended for newer tokens which have no direct docs
        Starting epoch 
        """
        if not self.second:
            return None
        try:
            decoded = base64.b64decode(self.second)
            return (int.from_bytes(decoded, byteorder="big") + self.epoch) / 1000
        except Exception as e:
            decoded = base64.b64decode(self.second + "==")
            return (int.from_bytes(decoded, byteorder="big") + self.epoch) / 1000
