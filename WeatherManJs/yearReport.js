const fs = require('fs')
const csvToJson = require('./csvToJson.js')

const WEATHER_FILES = fs.readdirSync('weatherfiles')
const generateYearReport = async year =>{
    const yearRecords = []
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
                    yearRecords.push(record)
                }
            }
        }
    }
    if (!yearRecords.length) {
        return
    }
    let result = getYearReport(yearRecords)
    printYearReport(result)
}

const getYearReport = records => {
    const maxTemp = getMaxTemp(records)
    const minTemp = getMinTemp(records)
    const maxHumid = getMaxHumidty(records)
    return { maxTemp, minTemp, maxHumid }
}

const printYearReport = report => {
    console.log(`Highest: ${report.maxTemp['Max TemperatureC']}C on ${report.maxTemp.PKT}`)
    console.log(`Lowest: ${report.minTemp['Min TemperatureC']}C on ${report.minTemp.PKT}`)
    console.log(`Humidity: ${report.maxHumid['Max Humidity']}% on ${report.maxHumid.PKT}`)
}

const getMaxTemp = weatherRecords => {
    let maxTemp = weatherRecords.reduce((previous, current) => {
        return (+previous['Max TemperatureC'] > +current['Max TemperatureC']) ? previous : current
    })
    return maxTemp
}

const getMinTemp = weatherRecords => {
    let minTemp = weatherRecords.reduce((previous, current) => {
        return (+previous['Min TemperatureC'] < +current['Min TemperatureC']) ? previous : current
    })
    return minTemp
}

const getMaxHumidty = weatherRecords => {
    let maxHumid = weatherRecords.reduce((previous, current) => {
        return (+previous['Max Humidty'] > +current['Max Humidity']) ? previous : current
    })
    return maxHumid
}

module.exports = generateYearReport
