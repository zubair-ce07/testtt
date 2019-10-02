import { plusSymbol, minusSymbol } from '../utils/constants'
export const getReport = weatherRecords => {
    const timeKey = 'PKT' in weatherRecords[1]? 'PKT': 'PKST';

    let chart = {};
    weatherRecords.forEach((weatherRecord) => {
        let minTemp = weatherRecord['Min TemperatureC'];
        let maxTemp = weatherRecord['Max TemperatureC'];
        let chartBar = `${minTemp} ${printChars(minTemp, minusSymbol)}`;
        chartBar += `${printChars(maxTemp, plusSymbol)} ${maxTemp}`;
        chart[weatherRecord[timeKey]] = chartBar;
    });

    return chart
};

const printChars = (numOfCharsToPrint, char) => {
    let chars = '';
    for (let n = 0; n < Math.abs(+numOfCharsToPrint); n++) {
        chars += char;
    }
    return chars;
};