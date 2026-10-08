import re
def get_log(filepath:str, level:list[str] = ["DEBUG","INFO","WARN","ERROR"])->list[str]:
    """Читает файл лога и возвращает отфильтрованный список строк.

        Args:
            filepath: Путь к файлу лога.
            level: Список уровней для фильтрации. Допустимые значения:
                "DEBUG", "INFO", "WARN", "ERROR". По умолчанию — все уровни.

        Returns:
            listed_log: Список строк вида "{время} {уровень} {сообщение}".

        Raises:
            TypeError: Если filepath не строка или level не список.
            ValueError: Если level пуст или содержит недопустимые значения.
            FileNotFoundError: Если файл по указанному пути не найден.
            OSError: При прочих ошибках ввода-вывода.
        """
    listed_log = []

    if type(filepath) != str:
        raise TypeError("Путь должен быть строкой.")

    if type(level) != list:
        raise TypeError("Уровни должны быть списком строк.")

    if not level or any([i not in ["DEBUG","INFO","WARN","ERROR"] for i in level]):
        raise ValueError("Некорректное значение списка уровней.")

    date_format = r"((2\d{3}-(((0[13578])|(1[02]))-((0[1-9])|([12]\d)|(3[01])))|2\d{3}-(((0[469])|(11))-((0[1-9])|([12]\d)|(30)))|2\d{3}-02-((0[1-9])|(1\d)|(2[0-9]))))"
    time_format = r"((([01]\d)|(2[0-3])):([0-5]\d):([0-5]\d))"
    level_format = rf"\b({'|'.join([i for i in level])})\b"
    log_format = rf"{date_format} {time_format} {level_format} .*"

    try:
        with open(filepath,"r") as f:
            for line in f:
                if re.search(log_format, line):
                    listed_log.append(f"{'{'+re.search(time_format, line)[0]+'}'} {'{'+re.search(level_format, line)[0]+'}'} {'{'+line.rstrip()[re.search(level_format+r'\s*', line).end():]+'}'}")
        return listed_log

    except FileNotFoundError:
        raise FileNotFoundError("Некорректный путь.")

    except OSError as error:
        raise OSError(f"{error}") from error


def find_ip(log:list[str])->list[str]:
    """Фильтрует строки, содержащие корректный IPv4-адрес.

        Args:
            log: Список строк лога.

        Returns:
            sorted_log: Список строк, в которых найден IP-адрес.

        Raises:
            TypeError: Если log не является списком.
        """
    ip_expression = r"\b((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))(\.((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))){3}\b"
    sorted_log = []

    if type(log) != list:
        raise TypeError("Лог должен быть списком строк.")

    for line in log:
        if re.search(ip_expression, line):
            sorted_log.append(line)
    return sorted_log


path = "example_log.txt"
print("Строки лога с уровнем WARN или ERROR.\n")
leveled_log = get_log(path, level = ["WARN","ERROR"])
for i in leveled_log:
    print(i)
print("\nСтроки лога, содержащие IP.\n")
log = get_log(path)
ips = find_ip(log)
for i in ips:
    print(i)
