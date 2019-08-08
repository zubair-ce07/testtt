var utils = require('./../utils/common');

var HotelPage = function() {
    
    this.getHotelPageInfo = function() {
        return {
            singleHotelClass: ".resultWrapper",
            originDropdownSelector: "div[id$=-location-smartbox-dropdown]",
            searchResultSelector: "div[id=searchResultsList]",
            mapContentSelector: ".Hotels-Results-InlineTab.Hotels-Results-InlineMap",
            reviewSelector: ".Hotels-Results-InlineTab.Hotels-Results-InlineReviews",
            ratesSelector: ".Hotels-Results-InlineTab.Hotels-Results-InlineRates",
            goToMapSelector: ".Hotels-Results-HotelRightRailMap.open"
        };
    };

    this.getHotelSearchResult = function() {
        return element.all(by.css(this.getHotelPageInfo().singleHotelClass));
    };

    this.waitForSearchCompletion = function() {
        var EC = protractor.ExpectedConditions;
        browser.wait(EC.visibilityOf(element(by.css('.resultsContainer')).element(by.css('.finished'))), 10000, 'Error! Unable to load hotels list in selected origin');
    };

    this.getFirstHotelFromList = function() {
        return this.getHotelSearchResult().first();
    };

    this.getFirstHotelDetail = function() {
        return element.all(by.css(this.getHotelPageInfo().searchResultSelector))
            .first()
            .all(by.css(this.getHotelPageInfo().singleHotelClass))
            .first()
            .all(by.css('.Hotels-Results-InlineDetailTabs'));
    };

    this.getFirstHotelTitle = function() {
        return this.getFirstHotelFromList().all(by.css('button[id$=info-title]'));
    };

    this.getFirstHotelPhotos = function() {
        try {
            const firstHotelInfo = this.getFirstHotelDetail();
            if(firstHotelInfo.isPresent()) {
                return firstHotelInfo.first().all(by.css('.photoGrid')).first().all(by.css('.col-1-3'));
            }
        }
        catch(err) {
            utils.handleException('getFirstHotelPhotos'. err.message);
        }
    };

    this.getFirstHotelTab = function(tabName) {
        try {
            let tabId = '';
            if(tabName === 'map') {
                tabId = 'map'
            } 
            else if (tabName === 'review') {
                tabId = 'reviews';
            }
            else if (tabName === 'rates') {
                tabId = 'rates'
            }
            const tabSelector = `div[id$=-${tabId}]`;
            const result = this.getFirstHotelDetail()
                .first()
                .all(by.css("div[id$=-tabs]"))
                .first()
                .all(by.css(tabSelector))
                .first();

            return result;
        }
        catch(err) {
            utils.handleException('getFirstHotelTab'. err.message);
        }
        return null;
    };

    this.getGoToMap = function() {
        const goToMap = element(by.css('.collapsible-wrapper')).element(by.css('div[id$=-map]'));
        return goToMap;
    }
    this.verifyGoToMap = function() {
        const goToMap = element(by.css('.collapsible-wrapper')).element(by.css('div[id$=-map]'));
        goToMap.getText().then(function(value) {
            console.log('go to map button clicked');
            goToMap.click().then(function() {

                browser.sleep(10000).then(function() {
                    const mapContent = element(by.css('.Hotels-Results-HotelRightRailMap.open'));
                    expect(mapContent.isPresent()).toBe(true);
                });
                
            });
        });
    }
};

module.exports = HotelPage;