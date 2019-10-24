import {Config} from 'protractor';

export let config: Config = {
	framework: "mocha",
	mochaOpts: {
	  timeout: false
	},
	ignoreUncaughtExceptions: true,
	seleniumAddress: 'http://localhost:4444/wd/hub',
	capabilities: {
	'browserName': 'chrome',
    chromeOptions: {
      args: ['--disable-gpu', '--no-sandbox', '--disable-extensions', '--disable-dev-shm-usage']
    }
  },
	specs: [ 'testParam.js' ],
	params: {
		value: ''
	}
};
