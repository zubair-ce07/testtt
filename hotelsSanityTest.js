var hotelPage = require('./HotelPage.js');
var searchedHotelPage = require('./searchedHotelPage.js');

describe('Test hotels on kayak website', function () {


    it('should check the title of hotels page', function () {

        hotelPage.openHomePage();
        hotelPage.openHotelLink();

        expect(browser.getTitle()).toEqual(browser.params.hotleLinkTitle);

    });

    it('should check the guest field on hotels page', function () {

        hotelPage.setElement("guestField");
        expect(hotelPage.getFieldText()).toBe(browser.params.guestFieldText);
    });

    it('should check the origin field on hotels page', function () {

        hotelPage.setElement("originField");
        expect(hotelPage.isDisplayed(hotelPage.getElement("originField"))).toBe(true);
    });

    it('should check the start date field on hotels page', function () {

        hotelPage.setElement("startDateField");
        expect(hotelPage.isDisplayed(hotelPage.getElement("startDateField"))).toBe(true);
    });

    it('should check the end date field on hotels page', function () {

        hotelPage.setElement("endDateField");
        expect(hotelPage.isDisplayed(hotelPage.getElement("endDateField"))).toBe(true);
    });

    it('should verify the count of searched hotels with BCN origin', function () {

        hotelPage.searchHotels()
        var resultCount = searchedHotelPage.getSearchResultCount();
        expect(resultCount).toBeGreaterThanOrEqual(5);
    });

});