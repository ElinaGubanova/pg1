def get_matrix(n, m, vile):
    if n <= 0 or m <= 0:
        return []

    matrix = []

    for i in range(n):
        blank = []
        for j in range(m):
            blank.append(vile)
        matrix.append(blank)

    return matrix


result1 = get_matrix(2, 2, 10)

result2 = get_matrix(3, 5, 42)

result3 = get_matrix(4, 2, 13)

print(result1)

print(result2)

print(result3)
