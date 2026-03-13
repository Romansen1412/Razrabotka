numbers = []
count = 0

# Считываем три числа
while count < 3:
    try:
        num = float(input("Введите число: "))
        numbers.append(num)
        count += 1
    except ValueError:
        print("Ошибка! Введите число.")

print("Числа из интервала [1, 50]:")

i = 0
while i < 3:
    if numbers[i] >= 1 and numbers[i] <= 50:
        print(numbers[i])
    i += 1