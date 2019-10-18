const path = require('path');
const env = require('dotenv');
const { SpecReporter } = require('jasmine-spec-reporter');

env.config({ path: path.join(__dirname, '.env') });

exports.config = {
  seleniumAddress: process.env.SELENIUM_ADDRESS,
  specs: [`${__dirname}/specs/**/**.spec.ts`],
  multiCapabilities: [
    {
      browserName: 'chrome',
      chromeOptions: {
        mobileEmulation: {
          deviceName: 'Pixel 2',
        }
      }
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
  },
  beforeLaunch: () => {
    require('ts-node').register({
      project: path.join(__dirname, 'tsconfig.json')
    })
  }
};
