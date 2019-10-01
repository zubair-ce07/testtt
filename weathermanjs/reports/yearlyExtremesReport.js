export const getReport = weatherRecords => {
    const maxTemp = getExtremes(weatherRecords, 'Max TemperatureC', ">");
    const minTemp = getExtremes(weatherRecords, 'Min TemperatureC', "<");
    const maxHumidity = getExtremes(weatherRecords, 'Max Humidity', ">");

    return {
        "Highest Temperature": `${maxTemp["Max TemperatureC"]}C on ${maxTemp['PST']}`,
        "Lowest Temperature": `${minTemp["Min TemperatureC"]}C on ${minTemp['PST']}`,
        "Max Humidity": `${maxHumidity["Max Humidity"]}% on ${maxHumidity['PST']}`
    }
};

const compare = {
    ">": (arg1, arg2) => {return arg1 > arg2},
    "<": (arg1, arg2) => {return arg1 < arg2}
};

const getExtremes = (weatherRecords, key, cond) => {
    return weatherRecords.reduce((maxValueRecord, currentRecord) => {
        return (compare[cond](+maxValueRecord[key], +currentRecord[key]))? maxValueRecord: currentRecord
    })
};