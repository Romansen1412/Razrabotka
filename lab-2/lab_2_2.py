Stroka = input("Введите строку: ")
Counter = 0
New_Stroka = ""

for i in range(len(Stroka)):
    if Stroka[i] == ":":
        New_Stroka += "%"
        Counter += 1
    else:
        New_Stroka += Stroka[i]

print("Количество замен:", Counter)
print(New_Stroka)