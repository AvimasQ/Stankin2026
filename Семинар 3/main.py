import re
def get_sku(text: str, sku_expression:str = r"(\d{4}-[A-Z]{2})|([A-Z]{2}-\d{4}(-[A-Z]{3})?)") -> list(str|None):
    '''
    Выделяет артикулы заказов из текста.
    Формат артикула по-умолчанию: 1234-AB или BC-5678 или DE-1234-ABC

    Args:
        text: Текст, в котором нужно найти артикулы.
        sku_expression: Регулярное выражение для поиска артикула.

    Returns:
        Список артикулов (str) или None (если в строке совпадений нет).

    Raises:
        TypeError: text или sku_expression не являются строками.
        ValueError: sku_expression не является корректным регулярным выражением.
    '''
    skus = []
    if type(text) != str:
        raise TypeError

    if type(sku_expression) != str:
        raise TypeError

    if type(sku_expression) != str:
        raise TypeError

    try:
        re.compile(sku_expression)
    except re.error as error:
        raise ValueError(f"Некорректрое регулярное выражение: {error}") from error

    lines = text.splitlines()
    for line in lines:
        skus.append(re.search(sku_expression, line)[0] if re.search(sku_expression, line) else None)
    return skus



a = open("file.txt","r").read()
for sku in get_sku(a):
    print(sku)
