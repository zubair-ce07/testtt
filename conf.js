exports.config = {
    seleniumAddress: 'http://localhost:4444/wd/hub',
    specs: ['hotelCardsVerification.js'],
    capabilities: {
        browserName: 'chrome',
        chromeOptions: {
            args: [
                '--start-maximized','--headless'
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
        hotleLinkTitle: 'Hotels: Find Cheap Hotel Deals & Discounts - KAYAK',
        guestFieldText: '1 room, 2 guests'
    }
};
