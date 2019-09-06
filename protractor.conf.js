const path = require('path');
const env = require('dotenv');

// load environment variables
env.config({path: path.join(__dirname, '.env')});

exports.config = {
  seleniumAddress: process.env.SELENIUM_ADDRESS,
  specs: [`${__dirname}/specs/**/**.spec.ts`],
  multiCapabilities: [
    {
      browserName: 'chrome',
      chromeOptions: {
        args: ["--blink-settings=imagesEnabled=false"],
        // args: ["--headless", "--disable-gpu", "--blink-settings=imagesEnabled=false"]
      }
    }
  ],
  beforeLaunch: () => {
    require('ts-node').register({
      project: path.join(__dirname, 'tsconfig.json')
    })
  }
};
