from __future__ import annotations

import re
from dataclasses import dataclass

from app.users import User, ForeignUser, LocalUser


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._cross_border_count: int = 0

    def validate_user_id(self, user_id: str) -> int:
        try:
            user_id_int = int(user_id)
        except ValueError as exc:
            raise ValueError("Invalid user id: must be integer") from exc
        return user_id_int

    def validate_user_name(self, name: str) -> str:
        stripped_name = name.strip()
        if not stripped_name or stripped_name.isdigit():
            raise ValueError("Invalid user name: must contain letters")
        return stripped_name

    def validate_phone(self, phone: str) -> str:
        stripped_phone = phone.strip()
        if not re.fullmatch(r"\+\d+", stripped_phone):
            raise ValueError("Invalid phone format")
        return stripped_phone

    def create_user(self, user_id: str, name: str, phone: str) -> User:
        user_id_int = self.validate_user_id(user_id)
        validated_name = self.validate_user_name(name)
        validated_phone = self.validate_phone(phone)

        if validated_phone.startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(user_id_int, validated_name, validated_phone)
        else:
            return ForeignUser(user_id_int, validated_name, validated_phone)

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"  
        '''
        if raw_call.count(',') != 5:
            raise ValueError("Invalid call format: expected 6 comma-separated fields")

        parts = raw_call.split(',')
        if any(not p.strip() for p in parts):
            raise ValueError("Invalid call format: empty fields not allowed")

        (caller_id, caller_name, caller_phone, reciever_id, reciever_name, reciever_phone) = parts  
        caller = self.create_user(caller_id, caller_name, caller_phone)
        reciever = self.create_user(reciever_id, reciever_name, reciever_phone)

        active_call = ActiveCall(caller, reciever)
        self._active_calls.append(active_call)

        if active_call.is_cross_border:
            self._cross_border_count += 1

        return active_call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_count
