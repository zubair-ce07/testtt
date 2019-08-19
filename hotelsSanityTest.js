var hotelPage = require('./HotelPage.js');
var searchedHotelPage = require('./searchedHotelPage.js');
var mapViewPage = require('./mapViewPage.js');

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

    it('should display the searched hotel details in detail tab', function () {

        var hotelDetails = searchedHotelPage.getSearchedHotelDetails();
        
        expect(hotelDetails).toBe(true);
    });
    
    it('should display the searched hotel photos in detail tab', function () {

        expect(searchedHotelPage.isDisplayed(searchedHotelPage.photosContainer)).toBe(true);
    });
    
    it('should verify the searched hotel maps in map tab', function () {

        var hotelMap = searchedHotelPage.getSearchedHotelMaps();
        expect(hotelMap).toBe(true);
    });
    
    it('should verify the searched hotel reviews in reviews tab', function () {

        var hotelReviews = searchedHotelPage.getSearchedHotelReviews();
        expect(hotelReviews).toBe(true);
    });
    
    it('should verify the searched hotel rates in rates tab', function () {

        var hotelRates = searchedHotelPage.getSearchedHotelRates();
        expect(hotelRates).toBe(true);
    });

    it('should display map view', function () {
        
        mapViewPage.displayMapView();
        expect(mapViewPage.isDisplayed(mapViewPage.getElement("mapBtn"))).toBe(true);
    });
});