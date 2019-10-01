import yargs from 'yargs';
import { validateArgs } from '../utils/helper'

export const args = yargs
    .command('$0 <path> [options]', 'weatherman driver program', (yargs) => {
        yargs.positional('path', {
            describe: 'path to files',
            type: 'string'
        }).option('extremes', {
            alias: 'e',
            describe: 'use this option to get extremes report',
            type: 'string'
        }).option('averages', {
            alias: 'a',
            describe: 'use this option to get averages report',
            type: 'string'
        }).option('chart', {
            alias: 'c',
            describe: 'use this option to get charts report',
            type: 'string'
        })
    })
    .argv;