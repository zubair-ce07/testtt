// Protractor configuration file, see link for more information
// https://github.com/angular/protractor/blob/master/lib/config.ts

exports.config = {
    allScriptsTimeout: 120000, // Timeout of each script
    specs: [
      './e2e/tests/*.e2e-spec.ts'  // pattern for your tests
    ],
    baseUrl: 'https://www.kayak.com', // URL of your SUT
    capabilities: { 
      'browserName': 'chrome', // name of the browser you want to test in
      shardTestFiles: true,
      maxInstances: 3 // max number of browser instances to run parallel
    },
    maxSessions: 3, // max number of browser sessions to run
    directConnect: true, // No need to run selenium server for chrome and firefox
    framework: 'mocha', // The framework we want to use instead of say jasmine
    mochaOpts: { // Some reasonable mocha config
      reporter: "spec",
      slow: 3000,
      ui: 'bdd',
      timeout: 880000
    },
    beforeLaunch: function() { // If you're using type script then you need compiler options
       require('ts-node').register({
         project: 'tsconfig.json'
       });
     },
    onPrepare: function() { // making chai available globally. in your test use `const expect = global['chai'].expect;`
      browser.manage().window().maximize();
      var chai = require('chai');
      var chaiAsPromised = require("chai-as-promised");
      chai.use(chaiAsPromised);
      global.chai = chai;
    }
  };