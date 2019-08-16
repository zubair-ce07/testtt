exports.config = {
	seleniumAddress: 'http://localhost:4444/wd/hub',
	specs: ['task1.js'],
	capabilities: {
	    browserName: 'chrome',
	    chromeOptions: {
	        args: [
	            '--start-maximized'//,'--headless'
	        ]
	    }
	},
	framework: 'jasmine',

	//Also add jasmine node options.

	jasmineNodeOpts: {

	    defaultTimeoutInterval: 30000,


	},
	params: {
    	hotleLinkTitle: 'Hotels: Find Cheap Hotel Deals & Discounts - KAYAK'
  	}
};
