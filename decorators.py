def bold(func):
    def wrapper(str_):
        str_ = func(str_)
        return '<b> {0} </b>'.format(str_)

    return wrapper


def tag(name):
    def decorator(func):
        def wrapper(str_):
            str_ = func(str_)
            return '{tag} {str_} {tag}'.format(tag=name, str_=str_)

        return wrapper

    return decorator


def force_str(func):
    def wrapper(str_):
        return func(str_.decode("utf-8"))

    return wrapper


@bold
def to_bold(str_):
    return str_


@tag('<i>')
def to_tag(str_):
    return str_


@force_str
def print_str(str_):
    print(str_)


if __name__ == '__main__':
    print(to_bold("hammad"))
    print(to_tag("hammad"))
    print_str(b'hammad')
