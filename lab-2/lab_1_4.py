sum_numbers = 0
count = 0

print("Введите целые числа. Для завершения введите stop.")

while True:
    user_input = input("Введите число: ")
    if user_input == "stop":
        break
    try:
        num = int(user_input)
    except ValueError:
        print("Ошибка! Введите целое число.")
        continue

    sum_numbers = sum_numbers + num
    count = count + 1

print("Сумма чисел:", sum_numbers)
print("Количество чисел:", count)
