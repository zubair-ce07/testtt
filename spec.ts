import HotelsFrontPage from "./pages/HotelsFrontPage";
import {browser} from "protractor";
import {HotelSearchResultsPage} from "./pages/HotelSearchResultsPage";
import {MapPage} from "./pages/MapPage";

describe('Testing KAYAK hotel site', () => {
    browser.waitForAngularEnabled(false);
    const hotelsFrontPageObj = new HotelsFrontPage();
    const hotelSearchResultsPageObj = new HotelSearchResultsPage();
    const mapPageObj = new MapPage();

    hotelsFrontPageObj.loadKAYAKHomePage();
    hotelsFrontPageObj.goToHotelsFrontPage();

    it('Should display the origin field', async () => {
        expect(await hotelsFrontPageObj.isHotelsOriginVisible()).toEqual(true)
    });
    it('Should display the start date field', async () => {
        expect(await hotelsFrontPageObj.isHotelsStartDateVisible()).toEqual(true)
    });
    it('Should display the start date field', async () => {
        expect(await hotelsFrontPageObj.isHotelsEndDateVisible()).toEqual(true)
    });
    it('Should display ‘1 room, 2 guests’ in guests field', async () => {
        expect(await hotelsFrontPageObj.getGuestFieldText()).toEqual('1 room, 2 guests')
    });
    it('Should load hotels results page', async () => {
        await hotelsFrontPageObj.searchByNewHotelsOrigin();
        expect(await hotelSearchResultsPageObj.isHotelsResultPageLoaded()).toEqual(true)
    });
    it('Should display at least 5 hotel results',async () => {
        expect(await hotelSearchResultsPageObj.getTotalNumOfHotelsResults()).toBeGreaterThanOrEqual(5);
    });
    it('Should display hotel details section', async () => {
        await hotelSearchResultsPageObj.openHotelDetailsDropdown();
        expect(await hotelSearchResultsPageObj.isHotelDetailsDropdownVisible()).toEqual(true);
    });
    it('Should display hotel images in ‘Details’ section.', async () => {
        expect(await hotelSearchResultsPageObj.isDetailsTabPhotosVisible()).toEqual(true);
    });
    it('Should display map in ‘Map’ section.', async () => {
        expect(await hotelSearchResultsPageObj.isMapInMapTabVisible()).toEqual(true);
    });
    it('Should display reviews in ‘Reviews’ section', async () => {
        expect(await hotelSearchResultsPageObj.isReviewsInReviewsTabVisible()).toEqual(true)
    });
    it('Should display rates in ‘Rates’ section', async () => {
        expect(await hotelSearchResultsPageObj.isRatesInRatesTabVisible()).toEqual(true)
    });
    it('Should display map view',async () => {
        await mapPageObj.clickShowMap();
       expect(await mapPageObj.isMainMapViewVisible()).toEqual(true)
    });
    it('Should display left rail filters', async () => {
        expect(await mapPageObj.isHorizontalFiltersVisible()).toEqual(true)
    });
    it('Should display hotel info', async () => {
        expect(await mapPageObj.isHotelInfoVisible()).toEqual(true)
    });
    it('Should display hotel card on the left side', async () => {
       expect(await mapPageObj.isHotelCardVisible()).toEqual(true)
    });
    it('Should open provider page in new tab', async () => {
        let providerName = await mapPageObj.getBookingProviderName();
        providerName = providerName.toLowerCase();
        await mapPageObj.clickViewDealBtn();
        expect(await mapPageObj.isBookingProviderPageOpened(providerName)).toContain(providerName);
    });
});