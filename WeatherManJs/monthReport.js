const fs = require('fs')
const csvToJson = require('./csvToJson.js')

const WEATHER_FILES = fs.readdirSync('weatherfiles')
const generateMonthReport = async (year, month) => {
    const monthRecords = []
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
                    monthRecords.push(record)
                }
            }
        }
    }
    if (!monthRecords.length) {
        return
    }
    let result = getMonthReport(monthRecords)
    printMonthReport(result)
}

const getMonthReport = records => {
    const highestAvg = getHighestAvg(records)
    const lowestAvg = getLowestAvg(records)
    const avgHumidity = getAvgHumidity(records)
    return { highestAvg, lowestAvg, avgHumidity }
}

const printMonthReport = report => {
    console.log(`Highest Average: ${report.highestAvg}C`)
    console.log(`Lowest Average: ${report.lowestAvg}C`)
    console.log(`Average Mean Humidity: ${report.avgHumidity}%`)
}

const getHighestAvg = weatherRecords => {
    const highestAvg = (weatherRecords.reduce((previous, current) => {
        return previous + +current['Max TemperatureC']
    }, 0) / weatherRecords.length)
    return Math.round(highestAvg)
}

const getLowestAvg = weatherRecords => {
    const lowestAvg = (weatherRecords.reduce((previous, current) => {
        return previous + +current['Min TemperatureC']
    }, 0) / weatherRecords.length)
    return Math.round(lowestAvg)
}

const getAvgHumidity = weatherRecords => {
    const avgHumidity = (weatherRecords.reduce((previous, current) => {
        return previous + +current['Mean Humidity']
    }, 0) / weatherRecords.length)
    return Math.round(avgHumidity)
}

module.exports = generateMonthReport
