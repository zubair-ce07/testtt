import moment from 'moment';
const momondoHomepage = require('./pages/homePage');
describe('Protractor Demo App', function() {
    let SELECTED_DATE = '';
    momondoHomepage.loadHomePage();
    it('Should display ‘London (LON)’ in the origin field', function() {
        expect(momondoHomepage.getOrigin()).toEqual('London (LON)');
    });
    it('Should display ‘New York (NYC)’ in the destination field.', function() {
        expect(momondoHomepage.getDestination()).toEqual('New York (NYC)');
    });
    it('Should display ‘Sat 8/24’ in the departure date field', function() {
        expect(momondoHomepage.getDepartureDate()).toBe('Sat 8/24');
    });
    it('Should display ‘Sun 9/22’ in the return date field.', function() {
        expect(momondoHomepage.getReturnDate()).toBe('Sun 9/22');
    });
    it('Should display ‘1 Adult, Economy’ in travelers field', function() {
        expect(momondoHomepage.getTravelers()).toBe('1 Adult, Economy');
    });
    it('Should display ‘Estimated Price Graph’ below the search form', function() {
       expect(momondoHomepage.isGraphVisible()).toEqual(true);
    });
    it('Should display first half of estimated price graph',async function () {
        momondoHomepage.selectTripType('One-way');
        expect(momondoHomepage.getMainVisibleGraphCount('first_half')).toEqual(1);
    });
    it('Should display both graphs',async function () {
        momondoHomepage.selectTripType('Round-trip');
        momondoHomepage.selectDateFromCalendar();
        expect(momondoHomepage.getMainVisibleGraphCount('both')).toEqual(2);
    });
    it('Should display tooltip with price',function () {
        expect(momondoHomepage.getGraphBarTooltip()).toContain('USD');
    });
    it('Should highlight selected bar',async function () {
        SELECTED_DATE = await momondoHomepage.getNewDate();
        const newSelectGraphBar = await momondoHomepage.getNewSelectedGraphBar(SELECTED_DATE);
        expect(momondoHomepage.getSelectedBarStatus(newSelectGraphBar)).toContain('selected');
    });
    it('Should display Price of selected bar',async function () {
        const selectedBarStatus = await momondoHomepage.getSelectedBarPrice();
        expect(selectedBarStatus).toEqual(true);
    });
    it('Should display ‘Price shown are estimates per person”',function () {
        const selectedPriceTextShownStatus = momondoHomepage.getSelectedPriceTextShown();
        expect(selectedPriceTextShownStatus).toEqual(true);
    });
    it('Should display ‘Search these days’ button',function () {
        const searchBtnShown = momondoHomepage.isSearchBtnShown();
        expect(searchBtnShown).toEqual(true);
    });
    it('Should display updated date in first result’s details section',async function () {
        momondoHomepage.searchTheseDays();
        momondoHomepage.showDetails();
        const FirstResultDepartureDate = momondoHomepage.getDepartureDateFromDetailsPanel();
        const expectedDate = moment(SELECTED_DATE).format('ddd, MMM D');
        expect(FirstResultDepartureDate).toEqual(expectedDate);
    });
    it('Should display updated departure date',function () {
        const departureField = momondoHomepage.getDepartureDate();
        const expectedDate = moment(SELECTED_DATE).format('ddd M/D');
        expect(departureField.getText()).toBe(expectedDate);
    });
    it('Should not display ‘Price shown are estimates per person’ label',function () {
        expect(momondoHomepage.isPricesShownTextExist());
    });
    it('Should not display ‘Search these days’ button',function () {
        expect(momondoHomepage.isSearchTheseDaysButtonExist())
    })
});
