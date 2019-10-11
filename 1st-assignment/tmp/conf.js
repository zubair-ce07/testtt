"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.config = {
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
    specs: ['test.js']
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY29uZi5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL2NvbmYudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7QUFFVyxRQUFBLE1BQU0sR0FBVztJQUMzQixTQUFTLEVBQUUsT0FBTztJQUNsQixTQUFTLEVBQUU7UUFDWCxPQUFPLEVBQUUsS0FBSztLQUNiO0lBQ0Qsd0JBQXdCLEVBQUUsSUFBSTtJQUM5QixlQUFlLEVBQUUsOEJBQThCO0lBQy9DLFlBQVksRUFBRTtRQUNkLGFBQWEsRUFBRSxRQUFRO1FBQ3BCLGFBQWEsRUFBRTtZQUNYLElBQUksRUFBRSxDQUFDLGVBQWUsRUFBRSxjQUFjLEVBQUUsc0JBQXNCLEVBQUUseUJBQXlCLENBQUM7U0FDN0Y7S0FDQTtJQUNKLEtBQUssRUFBRSxDQUFFLFNBQVMsQ0FBRTtDQUNwQixDQUFDIn0=