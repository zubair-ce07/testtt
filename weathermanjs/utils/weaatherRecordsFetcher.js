import {parseCSVFiles} from "../parsers/csvParser";
import {args} from "../parsers/argsParser";


export const getWeatherRecords = async (fileNames) => {
    return filterRecords(await parseCSVFiles(args.path, fileNames));
};

export const filterRecords = (weatherRecords) => {
    let filteredRecords = [];
    for (let record of weatherRecords) {
        if (!record['Max TemperatureC'] || !record['Min TemperatureC'] || !record['Mean Humidity'])  {
            continue;
        }
        filteredRecords.push(record);
    }
    return filteredRecords;
};