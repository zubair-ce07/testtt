from cursor_colors import CursorColors
import matplotlib.pyplot as plt

class Chart:
    default_bar_colors = [color for color in CursorColors]

    @staticmethod
    def console_barchart(chart_bars, indices, bar_color=[]):
        """ Prints the bar-chart on the command line. """
        chart = ""
        bar_color = bar_color if bar_color else Chart.default_bar_colors

        for y_axis in range(len(indices)):
            for index, stack in enumerate(chart_bars):
                chart += str(indices[y_axis]) + " " + bar_color[index].value
                chart += '+' * stack[y_axis]
                chart += ' ' + str(stack[y_axis])
                chart += CursorColors.WHITE.value
                chart += "\n"

        print('-'*60)
        print(chart)
        print('-' * 60)

    @staticmethod
    def console_stackchart(chart_bars, indices, bar_colors=[]):
        """ Prints the stack-chart on the command line. """
        chart = ""
        bar_colors = Chart.default_bar_colors if len(bar_colors) == 0 \
            else bar_colors

        for y_axis in range(len(indices)):
            chart += indices[y_axis] + " "
            for index, stack in enumerate(chart_bars):
                chart += bar_colors[index].value
                chart += '+' * stack[y_axis]
                chart += CursorColors.WHITE.value
            chart += " "
            for index, stack in enumerate(chart_bars):
                chart += str(stack[y_axis])
                chart += "-" if index != len(chart_bars) - 1 else ""
            chart += "\n"
        print('-'*60)
        print(chart)
        print('-' * 60)

    @staticmethod
    def gui_barchart(chart_bars, x_axis_labels, legends, ytitle='untitled',
                     char_title='untitled'):
        """ Prints the bar-chart on the GUI. """
        indices = list(range(len(x_axis_labels)))
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
        graph_axis.set_xticklabels(x_axis_labels)
        graph_axis.legend(legend_tuple, legends)
        plt.savefig("Graph.pdf")

