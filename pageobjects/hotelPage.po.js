let HotelPage = function() {
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
            endDateSelector: "[id$=-dateRangeInput-display-end-inner]"
        }
    };

    this.openHomePage = () => {
        browser.get(this.getHotelPageInfo().kayakPageUrl);
    };

    this.clickHotelsPage = async () => {
        const link = element(by.linkText("Hotels"));
        await link.click();
    };

    this.isHotelPageDisplayed = async() => {
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

    this.getDateFields = () => {
        const { datepickerSelector, datepickerSubSelector, startDateSelector, endDateSelector } = this.getHotelPageInfo();
        const datepicker = element(by.css(datepickerSelector)).element(by.css(datepickerSubSelector));
        const startDate = datepicker.element(by.css(startDateSelector));
        const endDate = datepicker.element(by.css(endDateSelector));
        return {
            startDate,
            endDate
        };
    };

    this.setTextInOriginField = async (searchKeyword) => {
        const { originInputFieldSelector, originInputFieldSubSelector} = this.getHotelPageInfo();
        const originField = this.getOriginField();
        await originField.click();
        let inputField = element.all(by.css(originInputFieldSelector)).get(0).element(by.css(originInputFieldSubSelector));
        await inputField.sendKeys(searchKeyword);
        console.log(`origin ${searchKeyword} is typed`);
    };

    this.selectFirstOriginFromOriginsList = async () => {
        const list = element.all(by.css(this.getHotelPageInfo().originsListDropdownSelector)).first().all(by.css('li'));
        const originsFound = await list.count();
        console.log('total origins found: ',originsFound);
        await list.first().click();
    };
};

export default HotelPage;