import { Config, browser } from 'protractor';

export let config: Config = {
    seleniumAddress: 'http://localhost:4444/wd/hub',
    capabilities: {
        'browserName': 'firefox',
        firefoxOptions: {
            args: ['--headless']
        },
        'moz:firefoxOptions': {
            args: ['--headless']
        },
    },
    framework: 'mocha',
    specs: ['./specs/spec.js'],
    mochaOpts: {
        ui: 'bdd',
        reporter: 'dot',
        timeout: 60000,
        bail: true
    },
    onPrepare: function () {
        require('chai');
        require('babel-register');
        browser.ignoreSynchronization = true;
        browser.manage().window().maximize();
    }
};