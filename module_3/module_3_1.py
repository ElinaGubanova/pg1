calls = 0


def count_calls():
    global calls
    calls += 1


def string_info(string):
    count_calls()
    return len(string), string.upper(), string.lower()


def is_contains(string, list_to_search):
    count_calls()
    lowercase_string = string.lower()
    return lowercase_string in (item.lower() for item in list_to_search)


print(string_info('Develop'))
print(string_info('meaning'))
print(is_contains('Dream', ['eam', 'DrArA', 'drEAM', 'DrEam', 'Drean']))
print(is_contains('Clothes', ['clothing', 'Disclothes']))

print(calls)
