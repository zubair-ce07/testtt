from argparser import ArgParser


if __name__=="__main__":
    parser = ArgParser()
    parser.process_args()
    path, exts, avgs, charts = parser.get_args()

    print path
    print exts
    print avgs
    print charts
