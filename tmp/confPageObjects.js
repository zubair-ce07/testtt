"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const protractor_1 = require("protractor");
const path = require('path');
exports.config = {
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
        protractor_1.browser.waitForAngularEnabled(false);
        protractor_1.browser.driver.manage().window().maximize();
    },
    SELENIUM_PROMISE_MANAGER: false,
    specs: ['specPageObjects.js']
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY29uZlBhZ2VPYmplY3RzLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4vY29uZlBhZ2VPYmplY3RzLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7O0FBQUEsMkNBQTJDO0FBQzNDLE1BQU0sSUFBSSxHQUFHLE9BQU8sQ0FBQyxNQUFNLENBQUMsQ0FBQztBQUNsQixRQUFBLE1BQU0sR0FBVztJQUMzQixTQUFTLEVBQUUsT0FBTztJQUNsQixTQUFTLEVBQUU7UUFDVixPQUFPLEVBQUUsS0FBSztLQUNkO0lBQ0Qsd0JBQXdCLEVBQUUsSUFBSTtJQUM5QixlQUFlLEVBQUUsOEJBQThCO0lBQy9DLFlBQVksRUFBRTtRQUNkLGFBQWEsRUFBRSxRQUFRO0tBQ3RCO0lBQ0QsU0FBUyxFQUFFLEdBQUcsRUFBRTtRQUNmLG9CQUFPLENBQUMscUJBQXFCLENBQUMsS0FBSyxDQUFDLENBQUM7UUFDckMsb0JBQU8sQ0FBQyxNQUFNLENBQUMsTUFBTSxFQUFFLENBQUMsTUFBTSxFQUFFLENBQUMsUUFBUSxFQUFFLENBQUM7SUFDN0MsQ0FBQztJQUNELHdCQUF3QixFQUFFLEtBQUs7SUFDL0IsS0FBSyxFQUFFLENBQUUsb0JBQW9CLENBQUU7Q0FDL0IsQ0FBQyJ9