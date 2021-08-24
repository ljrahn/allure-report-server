

def some_func(**kwargs):
    name = kwargs['name']
    id = kwargs['id']
    print(name)
    print(id)


my_dict = {
    'name': 'joe',
    'id': 3
}

some_func(**my_dict)

