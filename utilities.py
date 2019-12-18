def draw_bar_graph(day, graph_limits, graph_colors, unit='C', draw_separately=False):
    upper_limit, lower_limit = graph_limits
    upper_limit_color, lower_limit_color = graph_colors

    lower_limit_bar = f"\033[0;{lower_limit_color};40m{int(lower_limit) * '+'}"
    upper_limit_bar = f"\033[0;{upper_limit_color};40m{int(upper_limit) * '+'}"

    if draw_separately:
        return f'{day} {upper_limit_bar} {upper_limit}{unit}\033[0;0m\n' \
               f'{day} {lower_limit_bar} {lower_limit}{unit}\033[0;0m'

    else:
        return f'{day} {lower_limit_bar}{upper_limit_bar} \033[0;0m {lower_limit}{unit} - {upper_limit}{unit}'
