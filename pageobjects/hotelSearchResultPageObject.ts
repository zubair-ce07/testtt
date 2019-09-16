import { protractor, browser, element, by, ElementFinder, ElementArrayFinder } from "protractor";
import {
    waitForElementPresence,
    waitForElementVisibility,
    getElementByCSS
} from '../utils/common';

class HotelSearchResultPageObject {
    readonly searchResultPageSelector: string = ".Base-Results-ResultsPage";
    readonly searchResultListSelector: string = ".resultsContainer";
    readonly searchResultListSelector2: string = ".finished";
    readonly singleHotelSelector: string = ".resultWrapper";
    readonly singleHotelDetailSelector: string = ".Hotels-Results-InlineDetailTabs";
    readonly singleHotelTitleSelector: string = "[id$=info-title]";
    readonly singleHotelAllPhotosSelector: string = ".photoGrid";
    readonly singleHotelSinglePhotoSelector: string = ".col-1-3";
    readonly mapContentSelector: string = ".Hotels-Results-InlineTab.Hotels-Results-InlineMap";
    readonly reviewSelector: string = ".Hotels-Results-InlineTab.Hotels-Results-InlineReviews";
    readonly ratesSelector: string = ".Hotels-Results-InlineTab.Hotels-Results-InlineRates";
    readonly goToMapButtonContainerSelector: string = ".collapsible-wrapper";
    readonly goToMapButtonSelector: string = "[id$=-map]";
    readonly goToMapSelector: string = ".Hotels-Results-HotelRightRailMap.open";

    waitForSearchCompletion = (): void => {
        const { searchResultListSelector, searchResultListSelector2 } = this;
        let EC = protractor.ExpectedConditions;
        browser.wait(EC.visibilityOf(element(by.css(searchResultListSelector)).element(by.css(searchResultListSelector2))), 100000, 'Error! Unable to load hotels list in selected origin');
    };

    getHotelSearchResultPage = (): ElementFinder => {
        return getElementByCSS(this.searchResultPageSelector);
    };

    getHotelSearchResult = (): ElementArrayFinder => {
        return element.all(by.css(this.singleHotelSelector));
    };

    openSingleHotelDetail = async (): Promise<ElementFinder> => {
        await this.clickFirstHotelTitle();
        return this.getFirstHotelDetail();
    };

    clickFirstHotelTitle = async (): Promise<void> => {
        const titleLink = this.getFirstHotelTitle();
        await titleLink.click();
        const clickedHotelTitle = await titleLink.getText();
        console.log(`hotel title clicked: "${clickedHotelTitle}"`);

        const hotelDetailSection = getElementByCSS(this.singleHotelSelector);
        waitForElementPresence(hotelDetailSection, 10000, 'Timeout Error! Unable to load first hotel detail in selected origin');
    };

    getFirstHotelFromHotelsList = (): ElementFinder => {
        return this.getHotelSearchResult().first();
    };

    getFirstHotelDetail = (): ElementFinder => {
        return element.all(by.css(this.singleHotelDetailSelector)).first();
    };

    getFirstHotelTitle = (): ElementArrayFinder => {
        return this.getFirstHotelFromHotelsList().all(by.css(this.singleHotelTitleSelector));
    };

    getFirstHotelPhotos = (): ElementArrayFinder => {
        const { singleHotelAllPhotosSelector, singleHotelSinglePhotoSelector } = this;
        const firstHotelDetail = this.getFirstHotelDetail();
        return firstHotelDetail.all(by.css(singleHotelAllPhotosSelector)).first().all(by.css(singleHotelSinglePhotoSelector));
    };

    openTab = async (tabName): Promise<ElementFinder> => {
        await this.clickHotelTab(tabName);
        return this.getTabContent(tabName);
    };

    clickHotelTab = async (tabName): Promise<void> => {
        const tab = this.getFirstHotelTab(tabName);
        const tabId = await tab.getAttribute("id");
        await element(by.css(`[id=${tabId}]`)).click();
        console.log(`${tabName} tab is clicked"`);
    };

    getTabContent = (tabName): ElementFinder => {
        const tabContent = element.all(by.css(this.singleHotelSelector))
            .first()
            .all(by.css(this.getTabContentSelectorByTabName(tabName))).first();
        waitForElementVisibility(tabContent, 10000, `Timeout Error! hotel tab ${tabName} is taking too long to appear`);
        return tabContent;
    };

    getTabId = (tabName): string => {
        let tabId: string = '';
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

    getTabContentSelectorByTabName = (tabName): string => {
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

    getFirstHotelTab = (tabName): ElementFinder => {
        const tabId = this.getTabId(tabName);
        const tabSelector = `[id$=-${tabId}]`;
        return this.getFirstHotelDetail()
            .all(by.css("[id$=-tabs]"))
            .first()
            .all(by.css(tabSelector))
            .first();
    };

    getGoToMap = async (): Promise<ElementFinder> => {
        await this.clickGoToMapButton();
        this.waitForGoToMapVisibility();
        return getElementByCSS(this.goToMapSelector);
    };

    clickGoToMapButton = async (): Promise<void> => {
        const { goToMapButtonContainerSelector, goToMapButtonSelector } = this;
        const goToMapButton = element(by.css(goToMapButtonContainerSelector)).element(by.css(goToMapButtonSelector));
        await goToMapButton.click();
    };

    waitForGoToMapVisibility = (): void => {
        const mapContent = getElementByCSS(this.goToMapSelector);
        waitForElementVisibility(mapContent, 10000, `Timeout Error! Large Map is taking too long to appear`);
        console.log('map content displayed');
    };
}

export default HotelSearchResultPageObject;