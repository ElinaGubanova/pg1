my_dict = {
    'Elena': 1997, 'Emma': 1999,
    'Mark': 1989, 'Alex': 1995
}

print(my_dict)
print(my_dict['Emma'])
print(my_dict.get('Liza'))

my_dict.update({
    'Danil': 1987,
    'Sofia': 1992
})

print(my_dict)
goof = my_dict.pop('Mark')
print(my_dict)
print(goof)

my_set = {
    46, 7777, 7 + 6,
    46, 13, 'Dogs', True,
    (25, 66, 9, 8)
}
print(my_set)
print(my_set.add(376))
print(my_set.add(22))
print(my_set)
print(my_set.remove(7777))
print(my_set)
