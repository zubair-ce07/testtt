def change_color(color):
    return f'\033[0;{color};40m'


def reset_color():
    return f'\033[0;0m'


def draw_bar_graph(day, upper_limit, lower_limit, upper_limit_color, lower_limit_color, unit, draw_separately=False):

    if draw_separately:
        return f'{day} {generate_graph(upper_limit, upper_limit_color)} {upper_limit}{unit}{reset_color()}\n' \
               f'{day} {generate_graph(lower_limit, lower_limit_color)} {lower_limit}{unit}{reset_color()}'

    else:
        return f'{day} {generate_graph(lower_limit, lower_limit_color)}' \
               f'{generate_graph(upper_limit, upper_limit_color)} ' \
               f'{reset_color()}{lower_limit}{unit} - {upper_limit}{unit}'


def generate_graph(points, color):
    return f"{change_color(color)}{int(points) * '+'}"
