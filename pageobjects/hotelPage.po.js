let HotelPage = function() {

    this.getHotelPageInfo = () => {
        return {
            kayakPageUrl: "https://www.kayak.com/",
            hotelPageUrl: "https://www.kayak.com/hotels",
            originSearchKeyword: "BCN",
            guestFieldText: "1 room, 2 guests",
            searchBtnSelector: "div[id$=-formGridSearchBtn]",
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
        return element(by.css("div[id$=-fieldGridLocationCol]")).element(by.css("div[id$=-location-display]"));
    };

    this.getGuestField = () => {
        return element(by.css("div[id$=-roomsGuestsAboveForm]")).element(by.css(".js-label"));
    };

    this.getDateFields = () => {
        let datepicker = element(by.css("div[id*=-fieldGridDatePickerCol]"));
        if(datepicker.isPresent()) {
            datepicker = datepicker.element(by.css("div[id$=-dateRangeInput-display]"));
        }
        const startDate = datepicker.element(by.css("div[id$=-dateRangeInput-display-start-inner]"));
        const endDate = datepicker.element(by.css("div[id$=-dateRangeInput-display-end-inner]"));
        return {
            startDate,
            endDate
        };
    };

    this.searchOriginsList = () => {
        const originField = this.getOriginField();
        originField.click();
        let inputField = element.all(by.css('div[id$=-location-textInputWrapper]'))
            .get(0)
            .element(by.css('input[id$=-location]'));
        inputField.sendKeys(this.getHotelPageInfo().originSearchKeyword).then(() => {
            console.log(`origin ${this.getHotelPageInfo().originSearchKeyword} is typed`);
        });
    };

    this.selectFirstOriginFromList = () => {
        const list = element.all(by.css('div[id$=-location-smartbox-dropdown]')).first().all(by.css('li'));
        list.count().then(function(txt) {
            console.log('total origins found: ',txt);
        });
        list.first().click();
    };
};

export default HotelPage;