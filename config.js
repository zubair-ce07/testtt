exports.config = {
    directConnect: true,
    capabilities: {
        'browserName': 'chrome'
    },
    specs: [
        'spec.ts'
    ],
    framework: 'mocha',
    mochaOpts: {
        reporter: "spec",
        slow: 3000,
        ui: 'bdd',
        timeout: 500000
    },

    beforeLaunch: () => {
        require('ts-node').register({
            project: require('path').join(__dirname, './tsconfig.json')
        });
    },
    onPrepare: () => {
        const global = require('protractor');
        const browser = global.browser;
        browser.waitForAngularEnabled(false);
    }
};