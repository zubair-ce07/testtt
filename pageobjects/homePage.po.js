var HomePage = function() {
    
    this.getHomePageInfo = function() {
        return {
            homePageUrl: "https://www.kayak.com/",
            hotelPageUrl: "https://www.kayak.com/hotels",
            originSearchKeyword: "BCN",
            guestFieldText: "1 room, 2 guests",
            searchBtnSelector: "div[id$=-formGridSearchBtn]",
        }
    };

    this.getHotelsPage = function() {
        browser.ignoreSynchronization = true;
        browser.get(this.getHomePageInfo().homePageUrl);
        const link = element(by.linkText("Hotels"));
        link.click();
    };

    this.getOriginField = function() {
        let originField = element(by.css("div[id$=-fieldGridLocationCol]"));
        if(originField.isPresent()) {
            originField = originField.element(by.css("div[id$=-location-display]"));
        }
        else {
            console.log('origin field is missing');
        }
        return originField;
    };

    this.getGuestField = function() {
        return element(by.css("div[id$=-roomsGuestsAboveForm]")).element(by.css(".js-label"));
    };

    this.getDateFields = function() {
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

    this.searchOriginsList = function(searchTerm) {
        const originField = this.getOriginField();
        originField.click();
        let inputField = element.all(by.css('div[id$=-location-textInputWrapper]'))
            .get(0)
            .element(by.css('input[id$=-location]'));
        inputField.sendKeys(searchTerm);
    };

    this.selectFirstOriginFromList = function() {
        // select first option from result set
        const list = element.all(by.css('div[id$=location-smartbox-dropdown]')).first().all(by.css('li'));
        list.count().then(function(txt) {
            console.log('total origins found: ',txt);
        });
        list.first().click();
    };
};

module.exports = HomePage;