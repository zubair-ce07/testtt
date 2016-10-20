from argparser import ArgParser
from reports import ReportGenerator

if __name__ == "__main__":
    parser = ArgParser()
    parser.process_args()
    path, exts, avgs, charts = parser.get_args()

    rep_gen = ReportGenerator(path)
    rep_gen.get_yearly_extremes_bulk(exts)
    rep_gen.get_monthly_avgs_bulk(avgs)
    rep_gen.draw_charts_bulk(charts)
