import { browser, element, by, ElementFinder } from "protractor";
import { getElementByCSS, waitForElementPresence } from "../utils/common";

class HotelPageObject {
    readonly kayakPageUrl: string = "https://www.kayak.com/";
    readonly hotelPageUrl: string = "https://www.kayak.com/hotels";
    readonly originSearchKeyword: string = "BCN";
    readonly guestFieldText: string = "1 room, 2 guests";
    readonly originFieldSelector: string = "[id$=-fieldGridLocationCol]";
    readonly originFieldSubSelector: string = "[id$=-location-display]";
    readonly originInputFieldSelector: string = "[id$=-location-textInputWrapper]";
    readonly originInputFieldSubSelector: string = "[id$=-location]";
    readonly originsListDropdownSelector: string = "[id$=-location-smartbox-dropdown]";
    readonly guestFieldSelector: string = "[id$=-roomsGuestsAboveForm]";
    readonly guestFieldSubSelector: string = ".js-label";
    readonly datepickerSelector: string = "[id*=-fieldGridDatePickerCol]";
    readonly datepickerSubSelector: string = "[id$=-dateRangeInput-display]";
    readonly startDateSelector: string = "[id$=-dateRangeInput-display-start-inner]";
    readonly endDateSelector: string = "[id$=-dateRangeInput-display-end-inner]";
    readonly searchButtonSelector: string = "[id$=-formGridSearchBtn]";
    readonly searchButtonSubSelector: string = ".SeparateIconAndTextButton";

    openHomePage = (): void => {
        browser.get(this.kayakPageUrl);
    };

    openHotelsPage = async (): Promise<void> => {
        const link = element(by.linkText("Hotels"));
        await link.click();
    };

    isHotelPageDisplayed = async (): Promise<boolean> => {
        const currentPageURL = await browser.getCurrentUrl();
        return currentPageURL === this.hotelPageUrl;
    };

    getOriginField = (): ElementFinder => {
        const { originFieldSelector, originFieldSubSelector } = this;
        return element(by.css(originFieldSelector)).element(by.css(originFieldSubSelector));
    };

    getGuestField = (): ElementFinder => {
        const { guestFieldSelector, guestFieldSubSelector } = this;
        return element(by.css(guestFieldSelector)).element(by.css(guestFieldSubSelector));
    };

    getTravelDatePickerField = (): ElementFinder => {
        const { datepickerSelector, datepickerSubSelector } = this;
        return element(by.css(datepickerSelector)).element(by.css(datepickerSubSelector));
    };

    getTravelStartDate = (): ElementFinder => {
        const { startDateSelector } = this;
        const datepicker = this.getTravelDatePickerField();
        return datepicker.element(by.css(startDateSelector));
    };

    getTravelEndDate = (): ElementFinder => {
        const { endDateSelector } = this;
        const datepicker = this.getTravelDatePickerField();
        return datepicker.element(by.css(endDateSelector));
    };

    setOriginToBCN = async (): Promise<void> => {
        await this.setTextInOriginField(this.originSearchKeyword);
        this.waitForOriginsListPresence();
        await this.selectFirstOriginFromOriginsList();
    };

    setTextInOriginField = async (searchKeyword): Promise<void> => {
        const { originInputFieldSelector, originInputFieldSubSelector } = this;
        const originField = this.getOriginField();
        await originField.click();
        let inputField = element.all(by.css(originInputFieldSelector)).get(0).element(by.css(originInputFieldSubSelector));
        await inputField.sendKeys(searchKeyword);
        console.log(`origin ${searchKeyword} is typed`);
    };

    waitForOriginsListPresence = (): void => {
        const { originsListDropdownSelector } = this;
        const originsListDropDown = getElementByCSS(originsListDropdownSelector);
        waitForElementPresence(originsListDropDown, 10000, 'Error! Unable to load hotel result page');
    };

    selectFirstOriginFromOriginsList = async (): Promise<void> => {
        const allOrigins = element.all(by.css(this.originsListDropdownSelector)).first().all(by.css('li'));
        const originsCount = await allOrigins.count();
        console.log('total origins found: ', originsCount);
        await allOrigins.first().click();
    };

    searchHotels = async (): Promise<void> => {
        await this.clickSearchHotelsButton();
    };

    clickSearchHotelsButton = async (): Promise<void> => {
        const { searchButtonSelector, searchButtonSubSelector } = this;
        const searchBtn = element(by.css(searchButtonSelector)).element(by.css(searchButtonSubSelector));
        await searchBtn.click();
    };
}

export default HotelPageObject;