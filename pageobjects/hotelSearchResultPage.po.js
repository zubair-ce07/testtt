import {
    waitForElementPresence,
    waitForElementVisibility,
    getElementByCSS
} from './../utils/common';

let HotelSearchResultPage = function () {

    this.searchResultPageSelector = ".Base-Results-ResultsPage";
    this.searchResultListSelector = ".resultsContainer";
    this.searchResultListSelector2 = ".finished";
    this.singleHotelSelector = ".resultWrapper";
    this.singleHotelDetailSelector = ".Hotels-Results-InlineDetailTabs";
    this.singleHotelTitleSelector = "[id$=info-title]";
    this.singleHotelAllPhotosSelector = ".photoGrid";
    this.singleHotelSinglePhotoSelector = ".col-1-3";
    this.mapContentSelector = ".Hotels-Results-InlineTab.Hotels-Results-InlineMap";
    this.reviewSelector = ".Hotels-Results-InlineTab.Hotels-Results-InlineReviews";
    this.ratesSelector = ".Hotels-Results-InlineTab.Hotels-Results-InlineRates";
    this.goToMapButtonContainerSelector = ".collapsible-wrapper";
    this.goToMapButtonSelector = "[id$=-map]";
    this.goToMapSelector = ".Hotels-Results-HotelRightRailMap.open";

    this.waitForSearchCompletion = () => {
        const { searchResultListSelector, searchResultListSelector2 } = this;
        let EC = protractor.ExpectedConditions;
        browser.wait(EC.visibilityOf(element(by.css(searchResultListSelector)).element(by.css(searchResultListSelector2))), 100000, 'Error! Unable to load hotels list in selected origin');
    };

    this.getHotelSearchResultPage = () => {
        return getElementByCSS(this.searchResultPageSelector);
    };

    this.getHotelSearchResult = () => {
        return element.all(by.css(this.singleHotelSelector));
    };

    this.openSingleHotelDetail = async () => {
        await this.clickFirstHotelTitle();
        return this.getFirstHotelDetail();
    };

    this.clickFirstHotelTitle = async () => {
        const titleLink = this.getFirstHotelTitle();
        await titleLink.click();
        const clickedHotelTitle = await titleLink.getText();
        console.log(`hotel title clicked: "${clickedHotelTitle}"`);

        const hotelDetailSection = getElementByCSS(this.singleHotelSelector);
        waitForElementPresence(hotelDetailSection, 10000, 'Timeout Error! Unable to load first hotel detail in selected origin');
    };

    this.getFirstHotelFromHotelsList = () => {
        return this.getHotelSearchResult().first();
    };

    this.getFirstHotelDetail = () => {
        return element.all(by.css(this.singleHotelDetailSelector)).first();
    };

    this.getFirstHotelTitle = () => {
        return this.getFirstHotelFromHotelsList().all(by.css(this.singleHotelTitleSelector));
    };

    this.getFirstHotelPhotos = () => {
        const { singleHotelAllPhotosSelector, singleHotelSinglePhotoSelector } = this;
        const firstHotelDetail = this.getFirstHotelDetail();
        return firstHotelDetail.all(by.css(singleHotelAllPhotosSelector)).first().all(by.css(singleHotelSinglePhotoSelector));
    };

    this.openTab = async (tabName) => {
        await this.clickHotelTab(tabName);
        return this.getTabContent(tabName);
    };

    this.clickHotelTab = async (tabName) => {
        const tab = this.getFirstHotelTab(tabName);
        const tabId = await tab.getAttribute("id");
        await element(by.css(`[id=${tabId}]`)).click();
        console.log(`${tabName} tab is clicked"`);
    };

    this.getTabContent = (tabName) => {
        const tabContent = element.all(by.css(this.singleHotelSelector))
            .first()
            .all(by.css(this.getTabContentSelectorByTabName(tabName))).first();
        waitForElementVisibility(tabContent, 10000, `Timeout Error! hotel tab ${tabName} is taking too long to appear`);
        return tabContent;
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

    this.getTabContentSelectorByTabName = function (tabName) {
        if (tabName === 'map') {
            return this.mapContentSelector;
        }
        else if (tabName === 'review') {
            return this.reviewSelector;
        }
        else if (tabName === 'rates') {
            return this.ratesSelector;
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

    this.getGoToMap = async () => {
        await this.clickGoToMapButton();
        this.waitForGoToMapVisibility();
        return getElementByCSS(this.goToMapSelector);
    };

    this.clickGoToMapButton = async () => {
        const { goToMapButtonContainerSelector, goToMapButtonSelector } = this;
        const goToMapButton = element(by.css(goToMapButtonContainerSelector)).element(by.css(goToMapButtonSelector));
        await goToMapButton.click();
    };

    this.waitForGoToMapVisibility = () => {
        const mapContent = getElementByCSS(this.goToMapSelector);
        waitForElementVisibility(mapContent, 10000, `Timeout Error! Large Map is taking too long to appear`);
        console.log('map content displayed');
    };
};

export default HotelSearchResultPage;