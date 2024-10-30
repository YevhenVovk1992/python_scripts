def dict_recursive_flatten_iterator(d: dict) -> tuple:
    """
    A function that iterates through a dictionary in depth. The dictionary should consist of dictionaries and lists.
    Iterator returns a tuple of key and value nested elements.
    :param d: dict with dicts and lists inside it
    :return: iterator with tuple. First element is key, second element is value of nested elements
    """
    for k, v in d.items():
        if isinstance(v, list):
            for i in v:
                if isinstance(i, dict):
                    yield from dict_recursive_flatten_iterator(i)

        if isinstance(v, dict):
            yield from dict_recursive_flatten_iterator(v)
        yield (k, v)