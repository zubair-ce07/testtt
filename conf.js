exports.config = {
    seleniumAddress: 'http://localhost:4444/wd/hub',
    specs: ['hotelsSanityTest.js'],
    capabilities: {
        browserName: 'chrome',
        chromeOptions: {
            args: [
                '--start-maximized'//,'--headless'
            ]
        }
    },
    framework: 'jasmine',
    jasmineNodeOpts: {
        defaultTimeoutInterval: 30000,
    },
    params: {
        kayakSiteLink : 'https://www.kayak.com/',
        hotels : 'Hotels',
        bcnKeys : 'BCN',
        bcnSearchResult : 'Barcelona-El Prat (BCN) - Barcelona, Spain',
        hotleLinkTitle: 'Hotels: Find Cheap Hotel Deals & Discounts - KAYAK',
        guestFieldText: '1 room, 2 guests'
    },
    onPrepare: function () {
        browser.ignoreSynchronization = true;
        
    }
};
