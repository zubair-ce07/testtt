const yargs = require('yargs')
var generateMonthReport = require('./monthReport.js')
var generateYearReport = require('./yearReport.js')

var isValidYear = (year) => {
    if (year === undefined || year < 2000 || year > 2100) {
        return false
    }
    return true
}

var isValidMonth = (month) => {
    if (month === undefined || month < 1 || month > 12) {
        return false
    }
    return true
}

var parseArguments = () => {
    yargs.command(
        ['yearly', '-y'],
        'Generate yearly report',
        yargs => {
            yargs.positional('year', {
                describe: 'Year for which report should be generated',
                type: 'number'
            })
        },
        argv => {
            if (!isValidYear(argv.year)) {
                console.error('Please specify a valid date!')
            }
            generateYearReport(argv.year)
        }
    )

    yargs.command(
        ['monthly'],
        'Generate monthly average report',
        yargs => {
            yargs.positional('year', {
                describe: 'Year for which average should be calculated',
                type: 'number'
            })
            yargs.positional('month', {
                describe: 'Month of year for which average should be calculated',
                type: 'number'
            })
        },
        argv => {
            if (!(isValidYear(argv.year) && isValidMonth(argv.month))) {
                console.error('Please specify a valid date!')
            }
            generateMonthReport(argv.year, argv.month)
        }
    )
    yargs.parse()
}

parseArguments()
