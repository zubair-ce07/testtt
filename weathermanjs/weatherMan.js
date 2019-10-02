import { args } from './parsers/argsParser';
import { getFileNames } from './utils/fileNamesFetcher'
import { getReport as getMonthlyAvgsReport } from './reports/monthlyAvgsReport'
import { getReport as getYearlyExtremesReport } from './reports/yearlyExtremesReport';
import { getReport as getMonthlyChartReport } from './reports/monthlyChartsReport';
import { getWeatherRecords } from "./utils/weaatherRecordsFetcher";

const getReport = (report, arg) => {
    const fileNames = getFileNames(args.path, arg);
    getWeatherRecords(fileNames)
        .then(report)
        .then(console.log)
        .catch(console.log);
};

if (args.a != null) {
    getReport(getMonthlyAvgsReport, args.a);
}

if (args.e != null) {
    getReport(getYearlyExtremesReport, args.e);
}

if (args.c != null) {
    getReport(getMonthlyChartReport, args.c);
}