const fs = require('fs')
var csvToJson = require('./csvToJson.js')

const WEATHER_FILES = fs.readdirSync('weatherfiles')
var generateYearReport = async (year) =>{
    const YEAR_RECORDS = []
    for (file of WEATHER_FILES) {
        if (file.includes(year)) {
            try {
                var weatherRecords = await csvToJson(`weatherfiles/${file}`)
            }
            catch (error) {
                console.log(error)
            }
            for (record of weatherRecords) {
                if (record['Max TemperatureC'] && record['Min TemperatureC'] && record['Max Humidity']) {
                    YEAR_RECORDS.push(record)
                }
            }
        }
    }
    if (!YEAR_RECORDS.length) {
        return
    }
    let result = getYearReport(YEAR_RECORDS)
    printYearReport(result)
}

var getYearReport = (records) => {
    let maxTemp = getMaxTemp(records)
    let minTemp = getMinTemp(records)
    let maxHumid = getMaxHumidty(records)
    return { 'maxTemp': maxTemp, 'minTemp': minTemp, 'maxHumid': maxHumid }
}

var printYearReport = (report) => {
    let maxTemp = report.maxTemp
    let minTemp = report.minTemp
    let maxHumid = report.maxHumid
    console.log(`Highest: ${maxTemp['Max TemperatureC']}C on ${maxTemp.PKT}`)
    console.log(`Lowest: ${minTemp['Min TemperatureC']}C on ${minTemp.PKT}`)
    console.log(`Humidity: ${maxHumid['Max Humidity']}% on ${maxHumid.PKT}`)
}

var getMaxTemp = (weatherRecords) => {
    let maxTemp = weatherRecords.reduce((previous, current) => {
        return (+previous['Max TemperatureC'] > +current['Max TemperatureC']) ? previous : current
    })
    return maxTemp
}

var getMinTemp = (weatherRecords) => {
    let minTemp = weatherRecords.reduce((previous, current) => {
        return (+previous['Min TemperatureC'] < +current['Min TemperatureC']) ? previous : current
    })
    return minTemp
}

var getMaxHumidty = (weatherRecords) => {
    let maxHumid = weatherRecords.reduce((previous, current) => {
        return (+previous['Max Humidty'] > +current['Max Humidity']) ? previous : current
    })
    return maxHumid
}
module.exports = generateYearReport
