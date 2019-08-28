import {expect,assert} from 'chai';
import HotelsFrontPage from "./pages/HotelsFrontPage";
import {HotelSearchResultsPage} from "./pages/HotelSearchResultsPage";
import {MapPage} from "./pages/MapPage";

describe('Hotels page', () => {
    const hotelsFrontPageObj = new HotelsFrontPage();
    const hotelSearchResultsPageObj = new HotelSearchResultsPage();
    const mapPageObj = new MapPage();
    hotelsFrontPageObj.goToHotelsFrontPage();
    it('Should display the origin field', async () => {
        expect(await hotelsFrontPageObj.isHotelsOriginVisible()).to.be.true;
    });
    it('Should display the start date field', async () => {
        expect(await hotelsFrontPageObj.isHotelsStartDateVisible()).to.be.true;
    });
    it('Should display the start date field', async () => {
        expect(await hotelsFrontPageObj.isHotelsEndDateVisible()).to.be.true;
    });
    it('Should display ‘1 room, 2 guests’ in guests field', async () => {
        expect(await hotelsFrontPageObj.getGuestFieldText()).to.equal('1 room, 2 guests')
    });
    it('Should load hotels results page', async () => {
        await hotelsFrontPageObj.searchByNewHotelsOrigin();
        expect(await hotelSearchResultsPageObj.isHotelsResultPageLoaded()).to.be.true;
    });
    it('Should display at least 5 hotel results',async () => {
        assert.isAtLeast(await hotelSearchResultsPageObj.getTotalNumOfHotelsResults(),5);
    });
    it('Should display hotel details section', async () => {
        await hotelSearchResultsPageObj.openHotelDetailsDropdown();
        expect(await hotelSearchResultsPageObj.isHotelDetailsDropdownVisible()).to.be.true;
    });
    it('Should display hotel images in ‘Details’ section.', async () => {
        expect(await hotelSearchResultsPageObj.isDetailsTabPhotosVisible()).to.be.true;
    });
    it('Should display map in ‘Map’ section.', async () => {
        expect(await hotelSearchResultsPageObj.isMapInMapTabVisible()).to.be.true;
    });
    it('Should display reviews in ‘Reviews’ section', async () => {
        expect(await hotelSearchResultsPageObj.isReviewsInReviewsTabVisible()).to.be.true;
    });
    it('Should display rates in ‘Rates’ section', async () => {
        expect(await hotelSearchResultsPageObj.isRatesInRatesTabVisible()).to.be.true;
    });
    it('Should display map view',async () => {
        await mapPageObj.clickShowMap();
       expect(await mapPageObj.isMainMapViewVisible()).to.be.true;
    });
    it('Should display left rail filters', async () => {
        expect(await mapPageObj.isHorizontalFiltersVisible()).to.be.true;
    });
    it('Should display hotel info', async () => {
        expect(await mapPageObj.isHotelInfoVisible()).to.be.true;
    });
    it('Should display hotel card on the left side', async () => {
       expect(await mapPageObj.isHotelCardVisible()).to.be.true;
    });
    it('Should open provider page in new tab', async () => {
        let providerName = await mapPageObj.getBookingProviderName();
        providerName = providerName.toLowerCase();
        await mapPageObj.clickViewDealBtn();
        expect(await mapPageObj.isBookingProviderPageOpened(providerName)).to.include(providerName);
    });
});