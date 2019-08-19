'use strict';

require('babel-register');

exports.config = {
    seleniumAddress: 'http://localhost:4444/wd/hub',
    capabilities: {
        'browserName': 'firefox',
        firefoxOptions: {
            args: ['--headless']
        },
        'moz:firefoxOptions': {
            args: [ '--headless' ]
        },
    },
    framework: 'jasmine',
    specs: ['./specs/spec.js'],
    jasmineNodeOpts: {
        isVerbose: true,
    },
    onPrepare: function () {
        browser.ignoreSynchronization = true;
        browser.manage().window().maximize();
    }
};