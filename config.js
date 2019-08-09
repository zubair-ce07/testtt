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
    /*jasmineNodeOpts: {
        defaultTimeoutInterval: 30000
    },*/
    onPrepare: function () {
        browser.manage().window().maximize();
        //browser.manage().timeouts().implicitlyWait(5000);
    }
};