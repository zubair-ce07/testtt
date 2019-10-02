import yargs from 'yargs';
import { validateMonthlyReportArgs, validateYearlyReportArgs } from '../utils/argsValidator'

export const args = yargs
    .command('$0 <path> [options]', 'weatherman driver program', (yargs) => {
        yargs.positional('path', {
            describe: 'path to files',
            type: 'string'
        }).options({
            'extremes': {
                alias: 'e',
                describe: 'use this option to get extremes report',
                type: 'string',
                check: validateYearlyReportArgs
            }, 'averages': {
                alias: 'a',
                describe: 'use this option to get averages report',
                type: 'string',
                check: validateMonthlyReportArgs
            }, 'chart': {
                alias: 'c',
                describe: 'use this option to get charts report',
                type: 'string',
                check: validateMonthlyReportArgs
            }
        })
    }).argv;