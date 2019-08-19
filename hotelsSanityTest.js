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
        expect(hotelPage.isDisplayedCheck(hotelPage.getElement("originField"))).toBe(true);
    });

    it('should check the start date field on hotels page', function () {

        hotelPage.setElement("startDateField");
        expect(hotelPage.isDisplayedCheck(hotelPage.getElement("startDateField"))).toBe(true);
    });

    it('should check the end date field on hotels page', function () {

        hotelPage.setElement("endDateField");
        expect(hotelPage.isDisplayedCheck(hotelPage.getElement("endDateField"))).toBe(true);
    });

    it('should verify the count of searched hotels with BCN origin', function () {

        hotelPage.searchHotels()
        var resultCount = searchedHotelPage.getSearchResultCount();
        expect(resultCount).toBeGreaterThanOrEqual(5);
    });

    it('should display the searched hotel details in detail tab', function () {

        var hotelDetailsView = searchedHotelPage.getSearchedHotelDetails();
        
        expect(hotelDetailsView).toBe(true);
    });
    
    it('should display the searched hotel photos in detail tab', function () {

        expect(searchedHotelPage.isDisplayedCheck(searchedHotelPage.photosContainer)).toBe(true);
    });
    
    it('should verify the searched hotel maps in map tab', function () {

        var hotelMapView = searchedHotelPage.getSearchedHotelMaps();
        expect(hotelMapView).toBe(true);
    });
    
    it('should verify the searched hotel reviews in reviews tab', function () {

        var hotelReviewsView = searchedHotelPage.getSearchedHotelReviews();
        expect(hotelReviewsView).toBe(true);
    });
    
    it('should verify the searched hotel rates in rates tab', function () {

        var hotelRatesView = searchedHotelPage.getSearchedHotelRates();
        expect(hotelRatesView).toBe(true);
    });

    it('should display map view', function () {
        
        var mapContainerView = mapViewPage.getMapView();
        expect(mapContainerView).toBe(true);
    });

    it('should hover the hotel marker and display summary card', function () {

        var summaryCardView = mapViewPage.getHotelSummaryCard() 
        expect(summaryCardView).toBe(true);
        
    }); 

    it('should verify card view of selected hotel ', function () {
        
        var hotelCardView = mapViewPage.getHotelDetailCard() 
        expect(hotelCardView).toBe(true);
        
    }); 

    it('should verify deals of selected hotel on next tab', function () {
        
        var dealsWindow = mapViewPage.getDealsWindow() 
        expect(dealsWindow).toBe(true);
        
    }); 
});