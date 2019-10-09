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
            args: ['--disable-gpu', '--no-sandbox', '--disable-extensions', '--disable-dev-shm-usage', 'disable-infobars=true', '--disable-popup-blocking'],
            'prefs': {
                'credentials_enable_service': false
            }
        }
    },
    specs: ['test.js']
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY29uZi5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL2NvbmYudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7QUFFVyxRQUFBLE1BQU0sR0FBVztJQUMzQixTQUFTLEVBQUUsT0FBTztJQUNsQixTQUFTLEVBQUU7UUFDWCxPQUFPLEVBQUUsS0FBSztLQUNiO0lBQ0Qsd0JBQXdCLEVBQUUsSUFBSTtJQUM5QixlQUFlLEVBQUUsOEJBQThCO0lBQy9DLFlBQVksRUFBRTtRQUNkLGFBQWEsRUFBRSxRQUFRO1FBQ3BCLGFBQWEsRUFBRTtZQUNoQixJQUFJLEVBQUUsQ0FBQyxlQUFlLEVBQUUsY0FBYyxFQUFFLHNCQUFzQixFQUFFLHlCQUF5QixFQUFFLHVCQUF1QixFQUFDLDBCQUEwQixDQUFDO1lBQzlJLE9BQU8sRUFBRTtnQkFDUiw0QkFBNEIsRUFBRSxLQUFLO2FBQ25DO1NBQ0M7S0FDRjtJQUNGLEtBQUssRUFBRSxDQUFFLFNBQVMsQ0FBRTtDQUNwQixDQUFDIn0=