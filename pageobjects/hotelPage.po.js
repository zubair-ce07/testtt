import { getElementByCSS, waitForElementPresence } from "../utils/common";

let HotelPage = function () {

    this.kayakPageUrl = "https://www.kayak.com/";
    this.hotelPageUrl = "https://www.kayak.com/hotels";
    this.originSearchKeyword = "BCN";
    this.guestFieldText = "1 room, 2 guests";
    this.originFieldSelector = "[id$=-fieldGridLocationCol]";
    this.originFieldSubSelector = "[id$=-location-display]";
    this.originInputFieldSelector = "[id$=-location-textInputWrapper]";
    this.originInputFieldSubSelector = "[id$=-location]";
    this.originsListDropdownSelector = "[id$=-location-smartbox-dropdown]";
    this.guestFieldSelector = "[id$=-roomsGuestsAboveForm]";
    this.guestFieldSubSelector = ".js-label";
    this.datepickerSelector = "[id*=-fieldGridDatePickerCol]";
    this.datepickerSubSelector = "[id$=-dateRangeInput-display]";
    this.startDateSelector = "[id$=-dateRangeInput-display-start-inner]";
    this.endDateSelector = "[id$=-dateRangeInput-display-end-inner]";
    this.searchButtonSelector = "[id$=-formGridSearchBtn]";
    this.searchButtonSubSelector = ".SeparateIconAndTextButton";

    this.openHomePage = () => {
        browser.get(this.kayakPageUrl);
    };

    this.openHotelsPage = async () => {
        const link = element(by.linkText("Hotels"));
        await link.click();
    };

    this.isHotelPageDisplayed = async () => {
        const currentPageURL = await browser.getCurrentUrl();
        return currentPageURL === this.hotelPageUrl;
    };

    this.getOriginField = () => {
        const { originFieldSelector, originFieldSubSelector } = this;
        return element(by.css(originFieldSelector)).element(by.css(originFieldSubSelector));
    };

    this.getGuestField = () => {
        const { guestFieldSelector, guestFieldSubSelector } = this;
        return element(by.css(guestFieldSelector)).element(by.css(guestFieldSubSelector));
    };

    this.getTravelDatePickerField = () => {
        const { datepickerSelector, datepickerSubSelector } = this;
        return element(by.css(datepickerSelector)).element(by.css(datepickerSubSelector));
    };

    this.getTravelStartDate = () => {
        const { startDateSelector } = this;
        const datepicker = this.getTravelDatePickerField();
        return datepicker.element(by.css(startDateSelector));
    };

    this.getTravelEndDate = () => {
        const { endDateSelector } = this;
        const datepicker = this.getTravelDatePickerField();
        return datepicker.element(by.css(endDateSelector));
    };

    this.setOriginToBCN = async () => {
        await this.setTextInOriginField(this.originSearchKeyword);
        this.waitForOriginsListPresence();
        await this.selectFirstOriginFromOriginsList();
    };

    this.setTextInOriginField = async (searchKeyword) => {
        const { originInputFieldSelector, originInputFieldSubSelector } = this;
        const originField = this.getOriginField();
        await originField.click();
        let inputField = element.all(by.css(originInputFieldSelector)).get(0).element(by.css(originInputFieldSubSelector));
        await inputField.sendKeys(searchKeyword);
        console.log(`origin ${searchKeyword} is typed`);
    };

    this.waitForOriginsListPresence = () => {
        const { originsListDropdownSelector } = this;
        const originsListDropDown = getElementByCSS(originsListDropdownSelector);
        waitForElementPresence(originsListDropDown, 10000, 'Error! Unable to load hotel result page');
    };

    this.selectFirstOriginFromOriginsList = async () => {
        const allOrigins = element.all(by.css(this.originsListDropdownSelector)).first().all(by.css('li'));
        const originsCount = await allOrigins.count();
        console.log('total origins found: ', originsCount);
        await allOrigins.first().click();
    };

    this.searchHotels = async () => {
        await this.clickSearchHotelsButton();
    };

    this.clickSearchHotelsButton = async () => {
        const { searchButtonSelector, searchButtonSubSelector } = this;
        const searchBtn = element(by.css(searchButtonSelector)).element(by.css(searchButtonSubSelector));
        await searchBtn.click();
    };
};

export default HotelPage;