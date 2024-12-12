immutable_var = 1, 45, 5 + 6, "red", True, 8 > 6, [3, 7, 89]
print(immutable_var)
# immutable_var [2] = 5 #кортеж не поддерживает обращение по элементам  и не изменяет элемнты

mutable_list = [2, 5, 23, 1956, 545, 5778]
print(mutable_list)
mutable_list[-1] = 3466
print(mutable_list)
