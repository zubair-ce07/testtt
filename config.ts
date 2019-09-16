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
    framework: 'jasmine',
    specs: ['./specs/spec.js'],
    jasmineNodeOpts: {
        isVerbose: true,
    },
    onPrepare: function () {
        require('babel-register');
        browser.ignoreSynchronization = true;
        browser.manage().window().maximize();
    }
};