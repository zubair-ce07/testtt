import { getElementByCSS, waitForElementPresence } from "../utils/common";

let HotelPage = function () {
    this.getHotelPageInfo = () => {
        return {
            kayakPageUrl: "https://www.kayak.com/",
            hotelPageUrl: "https://www.kayak.com/hotels",
            originSearchKeyword: "BCN",
            guestFieldText: "1 room, 2 guests",
            originFieldSelector: "[id$=-fieldGridLocationCol]",
            originFieldSubSelector: "[id$=-location-display]",
            originInputFieldSelector: "[id$=-location-textInputWrapper]",
            originInputFieldSubSelector: "[id$=-location]",
            originsListDropdownSelector: "[id$=-location-smartbox-dropdown]",
            guestFieldSelector: "[id$=-roomsGuestsAboveForm]",
            guestFieldSubSelector: ".js-label",
            datepickerSelector: "[id*=-fieldGridDatePickerCol]",
            datepickerSubSelector: "[id$=-dateRangeInput-display]",
            startDateSelector: "[id$=-dateRangeInput-display-start-inner]",
            endDateSelector: "[id$=-dateRangeInput-display-end-inner]",
            searchButtonSelector: "[id$=-formGridSearchBtn]",
            searchButtonSubSelector: ".SeparateIconAndTextButton",
        }
    };

    this.openHomePage = () => {
        browser.get(this.getHotelPageInfo().kayakPageUrl);
    };

    this.openHotelsPage = async () => {
        const link = element(by.linkText("Hotels"));
        await link.click();
    };

    this.isHotelPageDisplayed = async () => {
        const currentPageURL = await browser.getCurrentUrl();
        return currentPageURL === this.getHotelPageInfo().hotelPageUrl;
    };

    this.getOriginField = () => {
        const { originFieldSelector, originFieldSubSelector } = this.getHotelPageInfo();
        return element(by.css(originFieldSelector)).element(by.css(originFieldSubSelector));
    };

    this.getGuestField = () => {
        const { guestFieldSelector, guestFieldSubSelector } = this.getHotelPageInfo();
        return element(by.css(guestFieldSelector)).element(by.css(guestFieldSubSelector));
    };

    this.getTravelDatePickerField = () => {
        const { datepickerSelector, datepickerSubSelector } = this.getHotelPageInfo();
        return element(by.css(datepickerSelector)).element(by.css(datepickerSubSelector));
    };

    this.getTravelStartDate = () => {
        const { startDateSelector } = this.getHotelPageInfo();
        const datepicker = this.getTravelDatePickerField();
        return datepicker.element(by.css(startDateSelector));
    };

    this.getTravelEndDate = () => {
        const { endDateSelector } = this.getHotelPageInfo();
        const datepicker = this.getTravelDatePickerField();
        return datepicker.element(by.css(endDateSelector));
    };

    this.setOriginToBCN = async () => {
        await this.setTextInOriginField('BCN');
        this.waitForOriginsListPresence();
        await this.selectFirstOriginFromOriginsList();
    };

    this.setTextInOriginField = async (searchKeyword) => {
        const { originInputFieldSelector, originInputFieldSubSelector } = this.getHotelPageInfo();
        const originField = this.getOriginField();
        await originField.click();
        let inputField = element.all(by.css(originInputFieldSelector)).get(0).element(by.css(originInputFieldSubSelector));
        await inputField.sendKeys(searchKeyword);
        console.log(`origin ${searchKeyword} is typed`);
    };

    this.waitForOriginsListPresence = () => {
        const { originsListDropdownSelector } = this.getHotelPageInfo();
        const originsListDropDown = getElementByCSS(originsListDropdownSelector);
        waitForElementPresence(originsListDropDown, 10000, 'Error! Unable to load hotel result page');
    };

    this.selectFirstOriginFromOriginsList = async () => {
        const allOrigins = element.all(by.css(this.getHotelPageInfo().originsListDropdownSelector)).first().all(by.css('li'));
        const originsCount = await allOrigins.count();
        console.log('total origins found: ', originsCount);
        await allOrigins.first().click();
    };

    this.searchHotels = async () => {
        await this.clickSearchHotelsButton();
    };

    this.clickSearchHotelsButton = async () => {
        const { searchButtonSelector, searchButtonSubSelector } = this.getHotelPageInfo();
        const searchBtn = element(by.css(searchButtonSelector)).element(by.css(searchButtonSubSelector));
        await searchBtn.click();
    };
};

export default HotelPage;