from constants import Colors


def draw_bar_graph(day, graph_limits, graph_colors, unit='C', draw_separately=False):
    upper_limit, lower_limit = graph_limits
    upper_limit_color, lower_limit_color = graph_colors

    lower_limit_bar = f"{lower_limit_color}{int(lower_limit) * '+'}"
    upper_limit_bar = f"{upper_limit_color}{int(upper_limit) * '+'}"

    if draw_separately:
        return f'{day} {upper_limit_bar} {upper_limit}{unit}{Colors.RESET.value}\n' \
               f'{day} {lower_limit_bar} {lower_limit}{unit}{Colors.RESET.value}'

    else:
        return f'{day} {lower_limit_bar}{upper_limit_bar} \033[0;0m {lower_limit}{unit} - {upper_limit}{unit}'
