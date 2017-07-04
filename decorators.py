def bold(func):
    def wrapper(str_):
        return func('<b> {} </b>'.format(str_))

    return wrapper


def tag(name):
    def decorator(func):
        def wrapper(str_):
            return func('{tag} {str_} {tag}'.format(tag=name, str_=str_))

        return wrapper

    return decorator


def force_str(func):
    def wrapper(str_):
        return func(str_.decode("utf-8"))

    return wrapper


@bold
def print_str(str_):
    print(str_)


@tag('<i>')
def print_str1(str_):
    print(str_)


@force_str
def print_str2(str_):
    print(str_)




if __name__ == '__main__':
    print_str("hammad")
    print_str1("hammad")
    print_str2(b'hammad')
