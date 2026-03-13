# Ввод первого числа
while True:
    try:
        a = float(input("Введите первое число: "))
        break
    except ValueError:
        print("Ошибка! Введите число.")

# Второй ввод 
while True:
    try:
        b = float(input("Введите второе число: "))
        break
    except ValueError:
        print("Ошибка! Введите число.")

# Третий ввод
while True:
    try:
        c = float(input("Введите третье число: "))
        break
    except ValueError:
        print("Ошибка! Введите число.")

print("Минимальное число:", min(a, b, c))