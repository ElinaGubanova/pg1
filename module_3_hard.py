def calculate_structure_sum(data):
    element_sum = 0

    for elem in data:
        if isinstance(elem, (list, tuple, set)):
            element_sum += calculate_structure_sum(elem)
        elif isinstance(elem, dict):
            element_sum += calculate_structure_sum(elem.items())
        elif isinstance(elem, (int, float)):
            element_sum += elem
        elif isinstance(elem, str):
            element_sum += len(elem)

    return element_sum

data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]

result = calculate_structure_sum(data_structure)
print(result)
