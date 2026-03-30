from __future__ import annotations

from dataclasses import dataclass

from app.users import User
from app.users.foreign_user import ForeignUser
from app.users.local_user import LocalUser


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

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        
        caller_id, caller_name, caller_phone, reciever_id, reciever_name, reciever_phone = raw_call.split(",")
        caller = LocalUser(int(caller_id), caller_name, caller_phone) if caller_phone.startswith(LOCAL_PHONE_PREFIX) else ForeignUser(int(caller_id), caller_name, caller_phone)
        reciever = LocalUser(int(reciever_id), reciever_name, reciever_phone) if reciever_phone.startswith(LOCAL_PHONE_PREFIX) else ForeignUser(int(reciever_id), reciever_name, reciever_phone)

        active_call = ActiveCall(caller, reciever)
        self._active_calls.append(active_call)

        if active_call.is_cross_border:
            self._cross_border_count += 1

        return active_call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_count
