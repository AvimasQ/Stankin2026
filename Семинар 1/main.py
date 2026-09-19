def status(signal: float) -> str:
    """
    Выводит показания датчика и статус отслеживаемой коровы.

    Args:
        signal (float): выходной сигнал с датчика (диапазон 4-20 мА).

    Returns:
        string: показания датчика и статус отслеживаемой коровы.

    Raises:
        TypeError: неверный тип signal
        ValueError: signal не является положительным
    """
    if type(signal) != float:
        raise TypeError("Неверный тип сигнала")
    if signal < 0:
        raise ValueError("Отрицательное значение сигнала")
    result = f"Показания датчика {signal}мА,"
    if 0<signal<=3.9 or signal >= 20.1:
        return str(result + " датчик неисправен.")
    if signal == 0:
        return str(result + " датчик отключен.")

    current_temperature = (signal - 4)*(75)/(20-4)
    result += f" датчик исправен. Температура {current_temperature:.1f}°C."

    if current_temperature > 50:
        return str(result + " Корова жива?")
    if current_temperature > 39.6:
        return str(result + " Корова больна.")
    if current_temperature > 39.1:
        return str(result + " Корова перегрелась.")
    if current_temperature > 37.5:
        return str(result + " Корова в норме.")
    if current_temperature > 35:
        return str(result + " Корова замерзла.")
    else:
        return str(result + " Отвалился датчик или корова.")


for i in range(1,220):
    print(status(i/10))
