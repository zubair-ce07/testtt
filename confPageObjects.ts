import {Config, browser} from 'protractor';
const path = require('path');
export let config: Config = {
	framework: "mocha",
	mochaOpts: {
		timeout: false,
		reporter: 'mochawesome-screenshots',
		reporterOptions: {
			overwrite: true,
			takePassedScreenshot: false,
			clearOldScreenshots: true,
			shortScrFileNames: false,
			jsonReport: false,
			multiReport: false
		}
	},
	ignoreUncaughtExceptions: true,
	seleniumAddress: 'http://127.0.0.1:4444/wd/hub',
	capabilities: {
	'browserName': 'chrome'
	},
	onPrepare: () => {
		browser.waitForAngularEnabled(false);
		browser.driver.manage().window().maximize();
		return browser.getProcessedConfig().then(function(config) {
			if (config.specs.length > 0) {
				const spec = path.basename(config.specs[0]);
				process.env.MOCHAWESOME_REPORTTITLE = spec;
				process.env.MOCHAWESOME_REPORTFILENAME = spec;
			}
		});
	},
	SELENIUM_PROMISE_MANAGER: false,
	specs: [ 'specPageObjects.js' ]
};