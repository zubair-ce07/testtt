'use strict';

var searchedHotelPage = function () {
    var detailsContainer = element.all(by.css("[id*=detailsWrapper]")).first();
    var resultsContainer = element(by.css("[id = searchResultsList]"));
    var searchedResults = resultsContainer.all(by.css("[class*=Base-Results-HorizonResult]"));
    var photosContainer = element.all(by.css("[class*=col-photos]")).first();
    var hotelMap;

    var EC = protractor.ExpectedConditions;

    this.isDisplayed = async function (element) {
        return await element.isDisplayed();
    }

    this.getSearchResultCount = async function () {

        var resultCount = 0;
        browser.wait(EC.presenceOf(resultsContainer), 10000);

        var resultbox = element(by.css("[class *= normalResults]"));
        browser.wait(EC.presenceOf(resultbox), 10000);

        browser.wait(EC.presenceOf(results), 10000);

        resultCount = await results.count();

        return await resultCount
    }

    this.verifyMaps = async function () {
        var mapTab = this.detailsCon.all(by.css("[id*=map]")).first();
        browser.wait(EC.presenceOf(mapTab), 7000);

        await mapTab.click()

        var mapContainer = element.all(by.css("[id*=mapContainer]")).first();
        browser.wait(EC.visibilityOf(mapContainer), 15000);
        this.hotelMap = mapContainer.all(by.css("[class*=gm-style]")).first();
        return await hotelMap;

    }
}
module.exports = new searchedHotelPage();