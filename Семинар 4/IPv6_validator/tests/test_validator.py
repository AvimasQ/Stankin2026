import pytest

from IPv6_validator import *

def test_all_valid_fixture_ipv6(valid_ipv6):
    for ip in valid_ipv6:
        assert is_valid_ipv6(ip) is True, f"должен быть валидным: r{ip!r}"


def test_all_invalid_fixture_ipv6(invalid_ipv6):
    for ip in invalid_ipv6:
        assert is_valid_ipv6(ip) is False, f"должен быть невалидным: {ip!r}"
        
def test_all_valid_fixture_ipv6_zoned(valid_ipv6_zoned):
    for ip in valid_ipv6_zoned:
        assert is_valid_ipv6_zoned(ip) is True, f"должен быть валидным: r{ip!r}"


def test_all_invalid_fixture_ipv6_zoned(invalid_ipv6_zoned):
    for ip in invalid_ipv6_zoned:
        assert is_valid_ipv6_zoned(ip) is False, f"должен быть невалидным: {ip!r}"