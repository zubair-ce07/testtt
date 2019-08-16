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
        //defaultTimeoutInterval: 30000
    },
    onPrepare: function () {
        browser.ignoreSynchronization = true;
        browser.manage().window().maximize();
        //browser.manage().timeouts().implicitlyWait(5000);
    }
};