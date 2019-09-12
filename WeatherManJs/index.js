const yargs = require('yargs')
const generateMonthReport = require('./monthReport.js')
const generateYearReport = require('./yearReport.js')

const isValidYear = year => {
    return !(year === undefined || year < 2000 || year > 2100)
}

const isValidMonth = month => {
    return !(month === undefined || month < 1 || month > 12)
}

const parseArguments = () => {
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
                return
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
                return
            }
            generateMonthReport(argv.year, argv.month)
        }
    )
    yargs.parse()
}

parseArguments()
