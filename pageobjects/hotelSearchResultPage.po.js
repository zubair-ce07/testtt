import * as utils from './../utils/common';

let HotelSearchResultPage = function() {
    this.getHotelSearchPageInfo = () => {
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

    this.waitForOriginsListPresence = () => {
        const originDDSelector = this.getHotelSearchPageInfo().originDropdownSelector;
        const originsListDropDown= utils.getSingleElementByCSS(originDDSelector);
        utils.waitForElementPresence(originsListDropDown, 10000, 'Error! Unable to load hotel result page');
    };

    this.clickSearchHotelsButton = async () => {
        const searchBtn = element(by.css("div[id$=-formGridSearchBtn]")).element(by.css('.SeparateIconAndTextButton'));
        await searchBtn.click();
    };

    this.getHotelSearchResult = () => {
        return element.all(by.css(this.getHotelSearchPageInfo().singleHotelClass));
    };

    this.waitForSearchCompletion = () => {
        const hotelsList = utils.getSingleElementByCSS(this.getHotelSearchPageInfo().singleHotelClass);
        let EC = protractor.ExpectedConditions;
        browser.wait(EC.visibilityOf(element(by.css('.resultsContainer')).element(by.css('.finished'))), 100000, 'Error! Unable to load hotels list in selected origin');
        utils.waitForElementPresence(hotelsList, 10000, 'Error! Unable to load hotels in selected origin');
    };

    this.clickFirstHotelTitle = async () => {
        await this.getHotelSearchResult();
        const titleLink = this.getFirstHotelTitle();
        await titleLink.click();
        const clickedHotelTitle = await titleLink.getText();
        console.log(`hotel title clicked: "${clickedHotelTitle}"`);

        const hotelsSelector= utils.getSingleElementByCSS(this.getHotelSearchPageInfo().singleHotelClass);
        utils.waitForElementPresence(hotelsSelector, 10000, 'Error! Unable to load hotels in selected origin');
    };

    this.getFirstHotelFromList = () => {
        return this.getHotelSearchResult().first();
    };

    this.getFirstHotelDetail = () => {
        return element.all(by.css(this.getHotelSearchPageInfo().searchResultSelector))
            .first()
            .all(by.css(this.getHotelSearchPageInfo().singleHotelClass))
            .first()
            .all(by.css('.Hotels-Results-InlineDetailTabs'))
            .first();
    };

    this.getFirstHotelTitle = () => {
        return this.getFirstHotelFromList().all(by.css('button[id$=info-title]'));
    };

    this.getFirstHotelPhotos = () => {
        try {
            const firstHotelInfo = this.getFirstHotelDetail();
            //if(firstHotelInfo.isPresent()) {
                return firstHotelInfo.all(by.css('.photoGrid')).first().all(by.css('.col-1-3'));
            //}
        }
        catch(err) {
            utils.handleException('getFirstHotelPhotos'. err);
        }
    };

    this.getTabId = function(tabName) {
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
        return tabId;
    };

    this.getTabContentSelector = function(tabName) {
        if(tabName === 'map') {
            return this.getHotelSearchPageInfo().mapContentSelector;
        }
        else if (tabName === 'review') {
            return this.getHotelSearchPageInfo().reviewSelector;
        }
        else if (tabName === 'rates') {
            return this.getHotelSearchPageInfo().ratesSelector;
        }
    };

    this.getFirstHotelTab = function(tabName) {
        try {
            const tabId = this.getTabId(tabName);
            const tabSelector = `div[id$=-${tabId}]`;
            return this.getFirstHotelDetail()
                .all(by.css("div[id$=-tabs]"))
                .first()
                .all(by.css(tabSelector))
                .first();
        }
        catch(err) {
            utils.handleException('getFirstHotelTab'. err.message);
        }
        return null;
    };

    this.clickSelectedHotelTab = async (tabName) => {
        const tab = this.getFirstHotelTab(tabName);
        const tabId = await tab.getAttribute("id");
        await element(by.css(`div[id=${tabId}]`)).click();
        console.log(`${tabName} tab is clicked"`);
    };

    this.getTabContent = (tabName) => {
        const mapContent = element.all(by.css(this.getHotelSearchPageInfo().singleHotelClass))
            .first()
            .all(by.css(this.getTabContentSelector(tabName))).first();
        utils.waitForElementVisibility(mapContent, 10000, `Timeout Error! selected hotel tab ${tabName} is taking too long to appear`);
        return mapContent;
    };

    this.clickGoToMap = async() => {
        const goToMap = element(by.css('.collapsible-wrapper')).element(by.css('div[id$=-map]'));
        await goToMap.click();
    };

    this.getMap = () => {
        const mapContent = element(by.css(this.getHotelSearchPageInfo().goToMapSelector));
        utils.waitForElementVisibility(mapContent, 10000, `Timeout Error! Large Map is taking too long to appear`);
        console.log('map content displayed');
        return mapContent;
    };
};

export default HotelSearchResultPage;