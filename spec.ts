import chai from 'chai';
import chaiAsPromised from 'chai-as-promised'
chai.use(chaiAsPromised);
const expect = chai.expect;
const assert = chai.assert;

import HotelsFrontPage from "./pages/HotelsFrontPage";
import {HotelSearchResultsPage} from "./pages/HotelSearchResultsPage";
import {MapPage} from "./pages/MapPage";

describe('Hotels page', () => {
    const hotelsFrontPageObj = new HotelsFrontPage();
    const hotelSearchResultsPageObj = new HotelSearchResultsPage();
    const mapPageObj = new MapPage();
    hotelsFrontPageObj.goToHotelsFrontPage();
    it('Should display the origin field', () => {
        expect(hotelsFrontPageObj.isHotelsOriginVisible()).to.eventually.be.true;
    });
    it('Should display the start date field', () => {
        expect(hotelsFrontPageObj.isHotelsStartDateVisible()).to.eventually.be.true;
    });
    it('Should display the start date field', () => {
        expect(hotelsFrontPageObj.isHotelsEndDateVisible()).to.eventually.be.true;
    });
    it('Should display ‘1 room, 2 guests’ in guests field',() => {
        expect(hotelsFrontPageObj.getGuestFieldText()).to.eventually.equal('1 room, 2 guests')
    });
    it('Should load hotels results page', async () => {
        await hotelsFrontPageObj.searchByNewHotelsOrigin();
        expect(await hotelSearchResultsPageObj.isHotelsResultPageLoaded()).to.eventually.be.true;
    });
    it('Should display at least 5 hotel results',async () => {
        assert.isAtLeast(await hotelSearchResultsPageObj.getTotalNumOfHotelsResults(),5);
    });
    it('Should display hotel details section', async () => {
        await hotelSearchResultsPageObj.openHotelDetailsDropdown();
        expect(await hotelSearchResultsPageObj.isHotelDetailsDropdownVisible()).to.eventually.be.true;
    });
    it('Should display hotel images in ‘Details’ section.',() => {
        expect(hotelSearchResultsPageObj.isDetailsTabPhotosVisible()).to.eventually.be.true;
    });
    it('Should display map in ‘Map’ section.', () => {
        expect(hotelSearchResultsPageObj.isMapInMapTabVisible()).to.eventually.be.true;
    });
    it('Should display reviews in ‘Reviews’ section', () => {
        expect(hotelSearchResultsPageObj.isReviewsInReviewsTabVisible()).to.eventually.be.true;
    });
    it('Should display rates in ‘Rates’ section', () => {
        expect(hotelSearchResultsPageObj.isRatesInRatesTabVisible()).to.eventually.be.true;
    });
    it('Should display map view',async () => {
        await mapPageObj.clickShowMap();
        expect(mapPageObj.isMainMapViewVisible()).to.eventually.be.true;
    });
    it('Should display left rail filters', () => {
        expect(mapPageObj.isHorizontalFiltersVisible()).to.eventually.be.true;
    });
    it('Should display hotel info', () => {
        expect(mapPageObj.isHotelInfoVisible()).to.eventually.be.true;
    });
    it('Should display hotel card on the left side', () => {
        expect(mapPageObj.isHotelCardVisible()).to.eventually.be.true;
    });
    it('Should open provider page in new tab', async () => {
        let providerName = await mapPageObj.getBookingProviderName();
        providerName = providerName.toLowerCase();
        await mapPageObj.clickViewDealBtn();
        expect(mapPageObj.isBookingProviderPageOpened(providerName)).to.eventually.include(providerName);
    });
});