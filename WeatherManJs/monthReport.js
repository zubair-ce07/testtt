const fs = require('fs')
var csvToJson = require('./csvToJson.js')

const WEATHER_FILES = fs.readdirSync('weatherfiles')
var generateMonthReport = async (year, month) => {
    const MONTH_RECORDS = []
    const MONTH_NAMES = {
        '1': 'Jan',
        '2': 'Feb',
        '3': 'Mar',
        '4': 'Apr',
        '5': 'May',
        '6': 'Jun',
        '7': 'Jul',
        '8': 'Aug',
        '9': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }
    month = MONTH_NAMES[month]
    for (file of WEATHER_FILES) {
        if (file.includes(`_${year}_${month}`)) {
            try {
                var weatherRecords = await csvToJson(`weatherfiles/${file}`)
            }
            catch (error) {
                console.log(error)
            }
            for (record of weatherRecords) {
                if (record['Max TemperatureC'] && record['Min TemperatureC'] && record['Mean Humidity']) {
                    MONTH_RECORDS.push(record)
                }
            }
        }
    }
    if (!MONTH_RECORDS.length) {
        return
    }
    let result = getMonthReport(MONTH_RECORDS)
    printMonthReport(result)
}

var getMonthReport = (records) => {
    let highestAvg = getHighestAvg(records)
    let lowestAvg = getLowestAvg(records)
    let avgHumidity = getAvgHumidity(records)
    return { 'highestAvg': highestAvg, 'lowestAvg': lowestAvg, 'avgHumidity': avgHumidity }
}

var printMonthReport = (report) => {
    let highestAvg = report.highestAvg
    let lowestAvg = report.lowestAvg
    let avgHumidity = report.avgHumidity
    console.log(`Highest Average: ${highestAvg}C`)
    console.log(`Lowest Average: ${lowestAvg}C`)
    console.log(`Average Mean Humidity: ${avgHumidity}%`)
}

var getHighestAvg = (weatherRecords) => {
    var highestAvg = (weatherRecords.reduce((previous, current) => {
        return previous + +current['Max TemperatureC']
    }, 0) / weatherRecords.length)
    return Math.round(highestAvg)
}

var getLowestAvg = (weatherRecords) => {
    var lowestAvg = (weatherRecords.reduce((previous, current) => {
        return previous + +current['Min TemperatureC']
    }, 0) / weatherRecords.length)
    return Math.round(lowestAvg)
}

var getAvgHumidity = (weatherRecords) => {
    var avgHumidity = (weatherRecords.reduce((previous, current) => {
        return previous + +current['Mean Humidity']
    }, 0) / weatherRecords.length)
    return Math.round(avgHumidity)
}

module.exports = generateMonthReport
