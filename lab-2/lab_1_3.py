# Ввод числа m
while True:
    try:
        m = float(input("Введите число m: "))
        break
    except ValueError:
        print("Ошибка! Введите число.")

# Вывод последовательности
for i in range(1, 11):
    result = i * m
    print(result)