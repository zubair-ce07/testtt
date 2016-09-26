from cursor_colors import CursorColors
import matplotlib.pyplot as plt

class Chart:
    default_color_array = [color for color in CursorColors]

    @staticmethod
    def show_horizontal_barchart(chart_bars, indices, color_array=[]):
        chart = ""
        color_array = color_array if color_array else Chart.default_color_array

        for y_axis in range(len(indices)):
            for index, stack in enumerate(chart_bars):
                chart += str(indices[y_axis]) + " " + color_array[index].value
                chart += '+' * stack[y_axis]
                chart += ' ' + str(stack[y_axis])
                chart += CursorColors.WHITE.value
                chart += "\n"

        print(chart)

    @staticmethod
    def show_stackchart(chart_bars, indices, color_array=[]):
        chart = ""
        color_array = Chart.default_color_array if len(color_array) == 0 \
            else color_array

        for y_axis in range(len(indices)):
            chart += indices[y_axis] + " "
            for index, stack in enumerate(chart_bars):
                chart += color_array[index].value
                chart += '+' * stack[y_axis]
                chart += CursorColors.WHITE.value
            chart += " "
            for index, stack in enumerate(chart_bars):
                chart += str(stack[y_axis])
                chart += "-" if index != len(chart_bars) - 1 else ""
            chart += "\n"
        print(chart)

    @staticmethod
    def show_vertical_barchart(chart_bars, days, legends, ytitle='untitled',
                               char_title='untitled'):
        total_days = len(days)

        indices = list(range(total_days))
        width = 0.5  # the width of the bars
        figure, graph_axis = plt.subplots()
        bar_rect = []
        legend_tuple = ()

        for bar in chart_bars:
            temp_rect = graph_axis.bar(indices, bar, width)
            bar_rect.append(temp_rect)
            legend_tuple = legend_tuple + (temp_rect,)
        # add some text for labels, title and axes ticks
        graph_axis.set_ylabel(ytitle)
        graph_axis.set_title(char_title)
        graph_axis.set_xticks(indices + [width])
        graph_axis.set_xticklabels(days)
        graph_axis.legend(legend_tuple, legends)
        plt.savefig("Graph.pdf")

