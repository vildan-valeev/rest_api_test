async def get_sum(nums: list) -> float:
    """"""
    # если встречаются значения с точкой, запятой - приводим к общему виду float
    print(nums)
    buf = []
    for i in nums:
        if i is None:
            continue
        buf.append(i.replace(',', '.'))
    # проверяем тип, суммируем
    sum = 0
    for n in buf:
        f = float(n)
        try:
            if isinstance(f, float):
                sum += f
        except ValueError as ex:
            continue
    return sum