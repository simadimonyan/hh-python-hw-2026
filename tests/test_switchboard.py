import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


def test_register_call_invalid_format_too_few_fields() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError):
        switchboard.register_call("1,Ivan,+79990000000,2,John")


def test_register_call_invalid_format_too_many_fields() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError):
        switchboard.register_call("1,Ivan,+79990000000,2,John,+15551234567,extra_field")


def test_register_call_empty_string() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError):
        switchboard.register_call("")


def test_register_call_only_commas() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError):
        switchboard.register_call(",,,,,")


def test_register_call_invalid_format_numeric_fields() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError):
        switchboard.register_call("1,2,3,4,5,6")


def test_register_call_missing_fields_middle() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError):
        switchboard.register_call("1,,+79990000000,2,John,+15551234567")
