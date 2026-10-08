"""Проверяет адреса IPv6 на корректность"""

import re
from functools import lru_cache

def _consecutive_zeros(l:list[str])->int: #Вспомогательная функция для поиска кол-ва последовательных '0' в списке.
    cz = 0
    m = 0
    for i in l:
        if i=='0':
            cz+=1
        else:
            m = max(m,cz)
            cz = 0
    return max(m,cz)


#RFC 5952

_H_NZ = r'(?:(?:[1-9a-f])|(?:[1-9a-f][0-9a-f])|(?:[1-9a-f][0-9a-f]{2})|(?:[1-9a-f][0-9a-f]{3}))'    #ненулевой гексет
_H_Z = r'(?:0)'                                                                                     #нулевой гексет
_H = rf'(?:{_H_NZ}|{_H_Z})'                                                                         #любой гексет

_IPBASE = (r'(?:'                                                                                   #Тело IPv6
    rf'(?:{_H}:){{7}}{_H}'
    rf'|(?:{_H}:){{0,5}}{_H_NZ}::'
    rf'|(?:{_H}:){{0,4}}{_H_NZ}::{_H_NZ}'
    rf'|(?:{_H}:){{0,3}}{_H_NZ}::{_H_NZ}(?::{_H})?'
    rf'|(?:{_H}:){{0,2}}{_H_NZ}::{_H_NZ}(?::{_H}){{0,2}}'
    rf'|(?:{_H}:)?{_H_NZ}::{_H_NZ}(?::{_H}){{0,3}}'
    rf'|{_H_NZ}::{_H_NZ}(?::{_H}){{0,4}}'
    rf'|::{_H_NZ}(?::{_H}){{0,5}}'
    r'|::'
    r')')

_IPV6 = re.compile(_IPBASE)

def is_valid_ipv6(address:str)-> bool:
    """
    Проверяет, является ли строка адресом IPv6 по стандарту RFC 5952.

    Args:
        address: Строка, которую необходимо проверить.
    Returns:
         True при соответствии стандарту, иначе False.
    Raises:
        TypeError: Адрес должен являться строкой.
    """
    if not isinstance(address, str):
        raise TypeError('Адрес должен быть строкой.')
    if _IPV6.fullmatch(address):
        if '::' not in address:
            return _consecutive_zeros(address.split(':')) < 2
        left, right = address.split('::')
        left = left.split(':') if left else []
        right = right.split(':') if right else []
        length = len(left)+len(right)
        if _consecutive_zeros(left)<8-length and _consecutive_zeros(right)<=8-length:
            return True
    return False


#RFC 4007

_Z = r'(?:(?:%[A-Za-z0-9_.-]+)?)' # идентификатор зоны по-умолчанию

_IPV6_Z = re.compile(rf'({_IPBASE}){_Z}')

@lru_cache(maxsize=None) #Помогает избегать повторного компилирования _IPV6_Z_C при множественных вызовах
def _ipv6_z_c(zone_pattern: str) -> re.Pattern[str]:
    return re.compile(rf'({_IPBASE}){zone_pattern}')


def is_valid_ipv6_zoned(address:str, zone_pattern:str|None = None)-> bool:
    """
    Проверяет, является ли строка адресом IPv6 по стандарту RFC 5952, но допускает наличие идентификатора зоны по стандарту RFC 4007.
    Примечание: RFC 4007 не указывает формат строки идентификатора зоны.
    Формат идентификатора зоны по-умолчанию:
    (?:(?:%[A-Za-z0-9_.-]+)?)

    Args:
        address: Строка, которую необходимо проверить.
        zone_pattern: Строка, содержащая регулярное выражение идентификатора зоны; приклеивается на конец паттерна IPv6. По-умолчанию: (?:(?:%[A-Za-z0-9_.-]+)?)
    Returns:
         True при соответствии стандартам, иначе False.
    Raises:
        TypeError: Адрес должен являться строкой.
        TypeError: RE идентификатора зоны должен быть непустой строкой либо None.
        ValueError: RE идентификатора зоны некорректен
    """
    if not isinstance(address, str):
        raise TypeError('Адрес должен быть строкой.')

    if not isinstance(zone_pattern, str|None):
        raise TypeError('RE идентификатора зоны должен быть непустой строкой либо None.')

    if zone_pattern:
        try:
            _IPV6_Z_C = _ipv6_z_c(zone_pattern)
            m = _IPV6_Z_C.fullmatch(address)
            if m:
                return is_valid_ipv6(m.group(1))
            else:
                return False
        except re.error as e:
            raise ValueError(f'RE идентификатора зоны некорректен: {e}') from e

    m = _IPV6_Z.fullmatch(address)
    if m:
        return is_valid_ipv6(m.group(1))
    return False