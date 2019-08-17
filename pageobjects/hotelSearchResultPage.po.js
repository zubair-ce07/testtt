import {
    waitForElementPresence,
    waitForElementVisibility,
    getElementByCSS
} from './../utils/common';

let HotelSearchResultPage = function () {
    this.getHotelSearchPageInfo = () => {
        return {
            originDropdownSelector: "[id$=-location-smartbox-dropdown]",
            searchButtonSelector: "[id$=-formGridSearchBtn]",
            searchButtonSubSelector: ".SeparateIconAndTextButton",
            searchResultListSelector: ".resultsContainer",
            searchResultListSelector2: ".finished",
            singleHotelSelector: ".resultWrapper",
            singleHotelDetailSelector: ".Hotels-Results-InlineDetailTabs",
            singleHotelTitleSelector: "[id$=info-title]",
            singleHotelAllPhotosSelector: ".photoGrid",
            singleHotelSinglePhotoSelector: ".col-1-3",
            mapContentSelector: ".Hotels-Results-InlineTab.Hotels-Results-InlineMap",
            reviewSelector: ".Hotels-Results-InlineTab.Hotels-Results-InlineReviews",
            ratesSelector: ".Hotels-Results-InlineTab.Hotels-Results-InlineRates",
            goToMapButtonContainerSelector: ".collapsible-wrapper",
            goToMapButtonSelector: "[id$=-map]",
            goToMapSelector: ".Hotels-Results-HotelRightRailMap.open"
        };
    };

    this.waitForOriginsListPresence = () => {
        const { originDropdownSelector } = this.getHotelSearchPageInfo();
        const originsListDropDown = getElementByCSS(originDropdownSelector);
        waitForElementPresence(originsListDropDown, 10000, 'Error! Unable to load hotel result page');
    };

    this.clickSearchHotelsButton = async () => {
        const { searchButtonSelector, searchButtonSubSelector } = this.getHotelSearchPageInfo();
        const searchBtn = element(by.css(searchButtonSelector)).element(by.css(searchButtonSubSelector));
        await searchBtn.click();
    };

    this.getHotelSearchResult = () => {
        return element.all(by.css(this.getHotelSearchPageInfo().singleHotelSelector));
    };

    this.waitForSearchCompletion = () => {
        const { searchResultListSelector, searchResultListSelector2, singleHotelSelector } = this.getHotelSearchPageInfo();

        let EC = protractor.ExpectedConditions;
        browser.wait(EC.visibilityOf(element(by.css(searchResultListSelector)).element(by.css(searchResultListSelector2))), 100000, 'Error! Unable to load hotels list in selected origin');

        const hotelsList = getElementByCSS(singleHotelSelector);
        waitForElementPresence(hotelsList, 10000, 'Error! Unable to load hotels in selected origin');
    };

    this.clickFirstHotelTitle = async () => {
        await this.getHotelSearchResult();
        const titleLink = this.getFirstHotelTitle();
        await titleLink.click();
        const clickedHotelTitle = await titleLink.getText();
        console.log(`hotel title clicked: "${clickedHotelTitle}"`);

        const hotelsSelector = getElementByCSS(this.getHotelSearchPageInfo().singleHotelSelector);
        waitForElementPresence(hotelsSelector, 10000, 'Error! Unable to load hotels in selected origin');
    };

    this.getFirstHotelFromHotelsList = () => {
        return this.getHotelSearchResult().first();
    };

    this.getFirstHotelDetail = () => {
        return element.all(by.css(this.getHotelSearchPageInfo().singleHotelDetailSelector)).first();
    };

    this.getFirstHotelTitle = () => {
        return this.getFirstHotelFromHotelsList().all(by.css(this.getHotelSearchPageInfo().singleHotelTitleSelector));
    };

    this.getFirstHotelPhotos = () => {
        const { singleHotelAllPhotosSelector, singleHotelSinglePhotoSelector } = this.getHotelSearchPageInfo();
        const firstHotelInfo = this.getFirstHotelDetail();
        return firstHotelInfo.all(by.css(singleHotelAllPhotosSelector)).first().all(by.css(singleHotelSinglePhotoSelector));
    };

    this.getTabId = function (tabName) {
        let tabId = '';
        switch (tabName) {
            case 'map':
                tabId = 'map';
                break;
            case 'review':
                tabId = 'reviews';
                break;
            case 'rates':
                tabId = 'rates';
                break;
        }
        return tabId;
    };

    this.getTabContentSelector = function (tabName) {
        if (tabName === 'map') {
            return this.getHotelSearchPageInfo().mapContentSelector;
        }
        else if (tabName === 'review') {
            return this.getHotelSearchPageInfo().reviewSelector;
        }
        else if (tabName === 'rates') {
            return this.getHotelSearchPageInfo().ratesSelector;
        }
    };

    this.getFirstHotelTab = function (tabName) {
        const tabId = this.getTabId(tabName);
        const tabSelector = `[id$=-${tabId}]`;
        return this.getFirstHotelDetail()
            .all(by.css("[id$=-tabs]"))
            .first()
            .all(by.css(tabSelector))
            .first();
    };

    this.clickSelectedHotelTab = async (tabName) => {
        const tab = this.getFirstHotelTab(tabName);
        const tabId = await tab.getAttribute("id");
        await element(by.css(`[id=${tabId}]`)).click();
        console.log(`${tabName} tab is clicked"`);
    };

    this.getTabContent = (tabName) => {
        const mapContent = element.all(by.css(this.getHotelSearchPageInfo().singleHotelSelector))
            .first()
            .all(by.css(this.getTabContentSelector(tabName))).first();
        waitForElementVisibility(mapContent, 10000, `Timeout Error! selected hotel tab ${tabName} is taking too long to appear`);
        return mapContent;
    };

    this.clickGoToMap = async () => {
        const { goToMapButtonContainerSelector, goToMapButtonSelector } = this.getHotelSearchPageInfo();
        const goToMap = element(by.css(goToMapButtonContainerSelector)).element(by.css(goToMapButtonSelector));
        await goToMap.click();
    };

    this.getMap = () => {
        const mapContent = element(by.css(this.getHotelSearchPageInfo().goToMapSelector));
        waitForElementVisibility(mapContent, 10000, `Timeout Error! Large Map is taking too long to appear`);
        console.log('map content displayed');
        return mapContent;
    };
};

export default HotelSearchResultPage;