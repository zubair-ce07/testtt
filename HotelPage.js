'use strict';


var HotelPage = function () {

    var guestField;
    var originField;
    var startDateField;
    var endDateField;

    var EC = protractor.ExpectedConditions;
    var error;

    this.openHomePage = async function () {
        await browser.get(browser.params.kayakSiteLink);
    };

    this.openHotelLink = async function () {
        var link = element(by.linkText(browser.params.hotels));
        await link.click();
    };

    this.getFieldText =  function () {
        try {
            return  this.guestField.getText();
        } catch (error) {
            console.log(error);
        }
    };

    this.setElement = function (elem) {
        try {

            switch (elem) {
                case "guestField":
                    this.guestField = element.all(by.css("[id *= roomsGuestsAboveForm]")).first().element(by.css("[class *= _idj]"));
                    break;
                case "originField":
                    this.originField = element.all(by.css("[id *= location-display]")).first();
                    break;
                case "startDateField":
                    this.startDateField =  element(by.css("[id *= dateRangeInput-display-start]"));
                    break;
                case "endDateField":
                    this.endDateField =  element(by.css("[id *= dateRangeInput-display-end]"));
                    break;
            }
        } catch (error) {
            console.log(error)
        }
    }

    this.getElement = function (elem) {
        switch (elem) {
            case "guestField":
                return this.guestField;
            case "originField":
                return this.originField;
            case "startDateField":
                return this.startDateField;
            case "endDateField":
                return this.endDateField;
        }

    }


    this.isDisplayed =  function (elem) {
        try {
            return  elem.isDisplayed();
        } catch (error) {
            console.log(error);
        }

    }

    this.searchHotels = async function () {

        try {
            
            var resultCount = 0;
            var originFieldBox = element.all(by.css("[id *= location-display]")).first();
            browser.wait(EC.visibilityOf(originFieldBox), 3000);
            originFieldBox.click();

            var originTextBox = element.all(by.css("[id *= location-textInputWrapper]")).first().element(by.tagName('input'));
            browser.wait(EC.visibilityOf(originTextBox), 7000);
            originTextBox.sendKeys(browser.params.bcnKeys);

            var originList = element.all(by.css("[id *= location-smarty-content]")).first();

            browser.wait(EC.elementToBeClickable(originList), 5000);

            originList.all(by.tagName('li')).first().click();
            var searchBtn =  element(by.css("[id$=-formGridSearchBtn]")).element(by.tagName('button'));
            await searchBtn.click();
        } catch (error) {
            console.log(error);
        }

    }
};
module.exports = new HotelPage();