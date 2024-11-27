def get_multiplied_digits(number):
    str_number = str(number)

    if len(str_number) == 1:
        if int(str_number) == 0:
            return 1
        else:
            return int(str_number)

    first = int(str_number[0])

    return first * get_multiplied_digits(int(str_number[1:]))

result = get_multiplied_digits(40203)
print(result)

result2 = get_multiplied_digits(402030)
print(result2)

result3 = get_multiplied_digits(222)
print(result3)

result4 = get_multiplied_digits(6070809)
print(result4)

result5 = get_multiplied_digits(10)
print(result5)