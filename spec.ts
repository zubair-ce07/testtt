import HomePage from "./pages/HomePage.po";
import {browser} from "protractor";
import moment from 'moment';
describe('Protractor Demo App', () => {
    browser.ignoreSynchronization = true;
    let SELECTED_DATE = '';
    let homePageObj = new HomePage();
    homePageObj.loadHomePage();
    it('Should display ‘London (LON)’ in the origin field', () => {
        expect(homePageObj.getOrigin()).toEqual('London (LON)');
    });
    it('Should display ‘New York (NYC)’ in the destination field.', () => {
        expect(homePageObj.getDestination()).toEqual('New York (NYC)');
    });
    it('Should display ‘Sat 8/24’ in the departure date field', () => {
        expect(homePageObj.getDepartureDate()).toBe('Sat 8/24');
    });
    it('Should display ‘Sun 9/22’ in the return date field.', () => {
        expect(homePageObj.getReturnDate()).toBe('Sun 9/22');
    });
    it('Should display ‘1 Adult, Economy’ in travelers field', () => {
        expect(homePageObj.getTravelers()).toBe('1 Adult, Economy');
    });
    it('Should display ‘Estimated Price Graph’ below the search form', () => {
        expect(homePageObj.isGraphVisible()).toEqual(true);
    });
    it('Should display first half of estimated price graph', async () => {
        homePageObj.selectTripType('One-way');
        expect(homePageObj.getMainVisibleGraphCount('first_half')).toEqual(1);
    });
    it('Should display both graphs', async () => {
        homePageObj.selectTripType('Round-trip');
        homePageObj.selectDateFromCalendar();
        expect(homePageObj.getMainVisibleGraphCount('both')).toEqual(2);
    });
    it('Should display tooltip with price', () => {
        expect(homePageObj.getGraphBarTooltipText()).toContain('USD');
    });
    it('Should highlight selected bar',async () => {
        SELECTED_DATE = await homePageObj.getNewDate();
        const newSelectGraphBar = await homePageObj.getNewSelectedGraphBar(SELECTED_DATE);
        expect(homePageObj.getSelectedBarStatus(newSelectGraphBar)).toContain('selected');
    });
    it('Should display Price of selected bar',async () => {
        expect(homePageObj.isSelectedBarPriceVisible()).toEqual(true);
    });
    it('Should display ‘Price shown are estimates per person”', () => {
        expect(homePageObj.isSelectedPriceLabelVisible()).toEqual(true);
    });
    it('Should display ‘Search these days’ button', () => {
        expect(homePageObj.isSearchBtnVisible()).toEqual(true);
    });
    it('Should display updated date in first result’s details section', async () => {
        await homePageObj.searchTheseDays();
        await homePageObj.showDetails();
        const FirstResultDepartureDate = await homePageObj.getDepartureDateFromDetailsPanel();
        const expectedDate = moment(SELECTED_DATE).format('ddd, MMM D');
        expect(FirstResultDepartureDate).toEqual(expectedDate);
    });
    it('Should display updated departure date', () => {
        const flightDepartureDate = homePageObj.getDepartureDate();
        const expectedDate = moment(SELECTED_DATE).format('ddd M/D');
        expect(flightDepartureDate).toBe(expectedDate);
    });
    it('Should not display ‘Price shown are estimates per person’ label', () => {
        expect(homePageObj.isPricesShownLabelVisible());
    });
    it('Should not display ‘Search these days’ button', () => {
        expect(homePageObj.isSearchTheseDaysBtnVisible())
    })
});