exports.config = {
	seleniumAddress: 'http://localhost:4444/wd/hub',
	specs: ['assignment1.js'],
	capabilities: {
	    browserName: 'chrome',
	    chromeOptions: {
	        args: [
	            '--start-maximized','--headless'
	        ]
	    }
	},
	framework: 'jasmine',

	//Also add jasmine node options.

	jasmineNodeOpts: {

	    defaultTimeoutInterval: 30000,


	},
};
