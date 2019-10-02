export const getReport = weatherRecords => {
    const avgMaxTemp = getAverage(weatherRecords, 'Max TemperatureC');
    const avgMinTemp = getAverage(weatherRecords, 'Min TemperatureC');
    const avgHumidity = getAverage(weatherRecords, 'Mean Humidity')

    return {avgMaxTemp, avgMinTemp, avgHumidity}
};

const getAverage = (weatherRecords, key) => {
    return weatherRecords.reduce((sum, val) => {
        return sum + +(val[key])
    }, 0) / weatherRecords.length;
};