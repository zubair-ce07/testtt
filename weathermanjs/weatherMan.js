import { args } from './parsers/argsParser';
import { parseCSVFiles } from './parsers/csvParser'
import { getFileNames } from './parsers/filesFetcher'
import { getReport as getMonthlyAvgsReport } from './reports/monthlyAvgsReport'
import { getReport as getYearlyExtremesReport } from './reports/yearlyExtremesReport'
import {filterRecords} from "./utils/helper";

const getReport = {a: getMonthlyAvgsReport, e: getYearlyExtremesReport};


const getWeatherRecords = async (fileNames) => {
    return filterRecords(await parseCSVFiles(args.path, fileNames));
};

console.log(args);

if (args.a != null) {
    const fileNames = getFileNames(args.path, args.a);
    getWeatherRecords(fileNames)
        .then(getReport.a)
        .then(console.log);
}
if (args.e != null) {
    const fileNames = getFileNames(args.path, args.e);
    getWeatherRecords(fileNames)
        .then(getReport.e)
        .then(console.log);
}