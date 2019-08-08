exports.config = {
    seleniumAddress: 'http://localhost:4444/wd/hub',
    capabilities: {
        'browserName': 'firefox'
    },
    framework: 'jasmine',
    specs: ['./specs/spec.js'],
    jasmineNodeOpts: {
        defaultTimeoutInterval: 30000
    }/*,
    onPrepare: function () {
        browser.manage().window().maximize();
        browser.manage().timeouts().implicitlyWait(5000);
    }*/
};