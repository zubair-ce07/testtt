const path = require('path');
const env = require('dotenv');
const {SpecReporter} = require('jasmine-spec-reporter');

// load environment variables
env.config({path: path.join(__dirname, '.env')});

exports.config = {
  seleniumAddress: process.env.SELENIUM_ADDRESS,
  specs: [`${__dirname}/specs/**/**.spec.ts`],
  multiCapabilities: [
    {
      browserName: 'chrome',
    }
  ],
  onPrepare: function () {
    jasmine.getEnv().addReporter(
      new SpecReporter({
        displayFailuresSummary: true,
        displayFailuredSpec: true,
        displaySuiteNumber: true,
        displaySpecDuration: true
      })
    );

    return browser.driver.manage().window().maximize();
  },
  beforeLaunch: () => {
    require('ts-node').register({
      project: path.join(__dirname, 'tsconfig.json')
    })
  }
};
