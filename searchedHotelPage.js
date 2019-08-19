'use strict';

var searchedHotelPage = function () {
    var detailsContainer;
    var photosContainer;
    var resultsContainer;
    var hotelMap;

    var EC = protractor.ExpectedConditions;
    var error;

    this.isDisplayedCheck = function (elem) {
        try {
            return elem.isDisplayed();
        } catch (error) {
            console.log(error);
        }

    }
    this.setElement = function (elem) {
        switch (elem) {
            case "detailsContainer":
                this.detailsContainer = element.all(by.css("[id*=detailsWrapper]")).first()
                break;
            case "photosContainer":
                this.photosContainer = element.all(by.css("[class*=col-photos]")).first();
                break;
            case "resultsContainer":
                this.resultsContainer = element(by.css("[id = searchResultsList]"));
                break;
        }

    }
    this.getElement = function (elem) {
        switch (elem) {
            case "detailsContainer":
                return this.detailsContainer;
            case "photosContainer":
                return this.photosContainer;
        }

    }

    this.getSearchResultCount = async function () {

        var resultCount = 0;
        this.setElement("resultsContainer");

        browser.wait(EC.presenceOf(this.resultsContainer), 10000);

        var resultbox = element(by.css("[class *= normalResults]"));
        browser.wait(EC.presenceOf(resultbox), 10000);

        var results = this.resultsContainer.all(by.css("[class*=Base-Results-HorizonResult]"));
        browser.wait(EC.presenceOf(results), 10000);

        try {
            resultCount = await results.count();

            return await resultCount;
        } catch (error) {
            console.log(error);
        }
    }
    this.getSearchedHotelDetails = async function () {

        var resultbox = element(by.css("[class *= normalResults]"));
        browser.wait(EC.presenceOf(resultbox), 10000);

        var results = this.resultsContainer.all(by.css("[class*=Base-Results-HorizonResult]"));
        browser.wait(EC.presenceOf(results), 10000);

        var hotel = results.first();
        try {
            await hotel.click();
            this.setElement("detailsContainer");
            this.setElement("photosContainer");
            return this.detailsContainer.isDisplayed();
        } catch (error) {
            console.log(error);
        }
    }

    this.getSearchedHotelMaps = async function () {

        var mapTab = this.detailsContainer.all(by.css("[id*=map]")).first();
        browser.wait(EC.presenceOf(mapTab), 7000);
        try {
            await mapTab.click()
            var mapContainer = element.all(by.css("[id*=mapContainer]")).first();
            browser.wait(EC.visibilityOf(mapContainer), 15000);

            this.hotelMap = mapContainer.all(by.css("[class*=gm-style]")).first();
            return hotelMap.isDisplayed();
        } catch (error) {
            console.log(error);
        }
    }
    this.getSearchedHotelReviews = async function () {

        var reviewTab = this.detailsContainer.all(by.css("[id*=reviews]")).first();
        browser.wait(EC.visibilityOf(reviewTab), 7500);
        try {
            await reviewTab.click()

            var reviewContainer = element.all(by.css("[id*=reviewsContainer]")).first();
            browser.wait(EC.visibilityOf(reviewContainer), 3000);

            return reviewContainer.isDisplayed();
        } catch (error) {
            console.log(error);
        }
    }
    this.getSearchedHotelRates = async function () {

        var ratesTab = this.detailsContainer.all(by.css("[id*=rates]")).first();
        browser.wait(EC.visibilityOf(ratesTab), 6000);
        try {
            await ratesTab.click();

            var ratesContainer = element.all(by.css("[id*=ratesContainer]")).first();
            browser.wait(EC.visibilityOf(ratesContainer), 4000);

            return ratesContainer.isDisplayed();
        } catch (error) {
            console.log(error);
        }
    }

}
module.exports = new searchedHotelPage();