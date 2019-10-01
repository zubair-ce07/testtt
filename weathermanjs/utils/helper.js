export const validateArgs = (args) => {
    return true;
};

export const filterRecords = (weatherRecords) => {
    let filteredRecords = Array();
    for (let record of weatherRecords) {
        if (!record['Max TemperatureC'] || !record['Min TemperatureC'] || !record['Mean Humidity'])  {
            continue;
        }
        filteredRecords.push(record);
    }
    return filteredRecords;
};