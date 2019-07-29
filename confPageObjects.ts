import {Config, browser} from 'protractor';
const path = require('path');
export let config: Config = {
	framework: "mocha",
	mochaOpts: {
		timeout: false,
	},
	ignoreUncaughtExceptions: true,
	seleniumAddress: 'http://127.0.0.1:4444/wd/hub',
	capabilities: {
	'browserName': 'chrome'
	},
	onPrepare: () => {
		browser.ignoreSynchronization = true;
		browser.driver.manage().window().maximize();
	},
	SELENIUM_PROMISE_MANAGER: false,
	specs: [ 'specPageObjects.js' ]
};
