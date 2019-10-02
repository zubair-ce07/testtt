export const getReport = weatherRecords => {
    const maxTemp = getExtremes(weatherRecords, 'Max TemperatureC', ">");
    const minTemp = getExtremes(weatherRecords, 'Min TemperatureC', "<");
    const maxHumidity = getExtremes(weatherRecords, 'Max Humidity', ">");

    let timeKey = 'PKT' in maxTemp? 'PKT': 'PKST';

    return {
        "Highest Temperature": `${maxTemp["Max TemperatureC"]}C on ${new Date(maxTemp[timeKey]).toISOString()}`,
        "Lowest Temperature": `${minTemp["Min TemperatureC"]}C on ${new Date(minTemp[timeKey]).toISOString()}`,
        "Max Humidity": `${maxHumidity["Max Humidity"]}% on ${new Date(maxHumidity[timeKey]).toISOString()}`,
    }
};

const compare = {
    ">": (op1, op2) => op1 > op2,
    "<": (op1, op2) => op1 < op2
};

const getExtremes = (weatherRecords, key, cond) => {
    return weatherRecords.reduce((maxValueRecord, currentRecord) => {
        return (compare[cond](+maxValueRecord[key], +currentRecord[key]))? maxValueRecord: currentRecord
    })
};