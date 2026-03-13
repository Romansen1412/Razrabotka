import sys

# Проверка наличия аргументов
if len(sys.argv) == 1:
    print("Ошибка! Передайте числа через командную строку")
    exit()

numbers = []
i = 1

# Преобразование аргументов в числа
while i < len(sys.argv):
    try:
        num = int(sys.argv[i])
        numbers.append(num)
    except ValueError:
        print("Ошибка! Все аргументы должны быть целыми числами")
        exit()
    i = i + 1

# Поиск минимального элемента
minimum = min(numbers)
min_index = numbers.index(minimum)

print("Минимальный элемент:", minimum)
print("Индекс минимального элемента:", min_index)


print("Положительные числа:")
i = 0
while i < len(numbers):

    if numbers[i] > 0:
        print(numbers[i], end=" ")

    i = i + 1

print()


print("Отрицательные числа:")
i = 0
while i < len(numbers):

    if numbers[i] < 0:
        print(numbers[i], end=" ")

    i = i + 1

print()