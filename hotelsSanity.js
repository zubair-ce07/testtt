var hotelPage = require('./HotelPage.js');

describe('Test hotels on kayak website', function () {


    it('should check the title of hotels page', function () {

        hotelPage.openHomePage();
        hotelPage.openHotelLink();

        expect(browser.getTitle()).toEqual(browser.params.hotleLinkTitle);

    });

    it('should check the guest field on hotels page', function () {

        expect(hotelPage.getText(hotelPage.guestField)).toBe(browser.params.guestFieldText);
    });

    it('should check the origin field on hotels page', function () {

        expect(hotelPage.isPresent(hotelPage.originField)).toBe(true);
    });

    it('should check the start date field on hotels page', function () {

        expect(hotelPage.isPresent(hotelPage.startDateField)).toBe(true);
    });

    it('should check the end date field on hotels page', function () {

        expect(hotelPage.isPresent(hotelPage.endDateField)).toBe(true);
    });


});