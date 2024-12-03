def calculate_structure_sum(data):
    element_sum = 0

    for i in data:
        if isinstance(i, (int, float)):
            element_sum += i
        elif isinstance(i, str):
            element_sum += len(i)
        elif isinstance(i, list):
            element_sum += calculate_structure_sum(i)
        elif isinstance(i, tuple):
            element_sum += calculate_structure_sum(i)
        elif isinstance(i, dict):
            element_sum += calculate_structure_sum(i.items())

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
