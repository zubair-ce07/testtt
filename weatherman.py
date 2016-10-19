from argparser import ArgParser
from reports import ReportGenerator

if __name__=="__main__":
    parser = ArgParser()
    parser.process_args()
    path, exts, avgs, charts = parser.get_args()

    rep_gen = ReportGenerator(path)
    rep_gen.get_yearly_extremes(exts[0])
