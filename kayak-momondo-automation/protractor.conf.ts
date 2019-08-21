import { IConfig } from './src/core/interfaces/flight';
import { configArray } from './src/conf/config';
import { ProtractorBrowser, Config } from 'protractor';
export const config : Config = {
  allScriptsTimeout: 120000,
  specs: [
    './src/test-cases/*.spec.js',
  ],
  seleniumAddress: 'http://localhost:4444/wd/hub',
  directConnect: true,
  capabilities: {
    browserName: 'chrome',
    },
    params: {
      brand: '',
      flightPage : {},
  },
  framework: 'mocha',
  mochaOpts: { // Some reasonable mocha config
    reporter: 'spec',
    slow: 3000,
    ui: 'bdd',
    timeout: 880000,
  },
  beforeLaunch : () => { // If you're using type script then you need compiler options
  require('ts-node').register({
    project: 'tsconfig.json',
  });
},
  onPrepare: () => {
   const globals = require('protractor');
   const browser = globals.browser;
   browser.manage().window().maximize();
   browser.waitForAngularEnabled(false);
   configArray.forEach(( conf : IConfig ) => {
     if ( browser.params.brand ===  conf.brand) {
      browser.baseUrl = conf.url;
      browser.params.flightPage = conf.pageObject;
    }
  });
 },
};
