def print_params(a=1, b='строка', c=True):
    print(a, b, c)


print_params()
print_params(25)
print_params(c=[1, 2, 3])
print_params(3.56, 'hello', False)
print_params(b='новая строка')

values_list = [1, 'Door', False]
values_dict = {'a': 1, 'b': 'строка', 'c': True}
values_list_2 = [1.57, True]

print_params(*values_list)
print_params(**values_dict)
print_params(*values_list_2, 42)
