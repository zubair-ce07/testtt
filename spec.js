const moment = require('moment');
const momondoHomepage = require('./pages/homePage');
describe('Protractor Demo App', function() {
    // To ignore checking the angular app
    browser.ignoreSynchronization = true;
    let SELECTED_DATE = '';
    momondoHomepage.loadHomePage();
    // Step 1
    // 1)
    it('Should display ‘London (LON)’ in the origin field', function() {
        expect(momondoHomepage.getOrigin()).toEqual('London (LON)');
    });
    // 2)
    it('Should display ‘New York (NYC)’ in the destination field.', function() {
        expect(momondoHomepage.getDestination()).toEqual('New York (NYC)');
    });
    // 3)
    it('Should display ‘Sat 8/24’ in the departure date field', function() {
        expect(momondoHomepage.getDepartureDate()).toBe('Sat 8/24');
    });
    // 4)
    it('Should display ‘Sun 9/22’ in the return date field.', function() {
        expect(momondoHomepage.getReturnDate()).toBe('Sun 9/22');
    });
    // 5)
    it('Should display ‘1 Adult, Economy’ in travelers field', function() {
        expect(momondoHomepage.getTravelers()).toBe('1 Adult, Economy');
    });
    // 6)
    it('Should display ‘Estimated Price Graph’ below the search form', function() {
       expect(momondoHomepage.isGraphVisible()).toEqual(true);
    });


    // Step 2

    it('Should display first half of estimated price graph',async function () {
        momondoHomepage.selectTripType('One-way');
        expect(momondoHomepage.getMainVisibleGraphCount('first_half')).toEqual(1);
    });


    // Step 3

    it('Should display both graphs',async function () {
        momondoHomepage.selectTripType('Round-trip');
        momondoHomepage.selectDateFromCalendar();
        expect(momondoHomepage.getMainVisibleGraphCount('both')).toEqual(2);
    });

    // Step 4

    it('Should display tooltip with price',function () {
        expect(momondoHomepage.hoverOverGraphBar().getText()).toContain('USD');
    });

    // Step 5

    // 1)
    it('Should highlight selected bar',async function () {
        // Getting date of two days after than currently selected one
        SELECTED_DATE = await momondoHomepage.getNewDate();
        // Getting new Selected bar
        const newSelectGraphBar = await momondoHomepage.getNewSelectedGraphBar(SELECTED_DATE);
        // Getting status of the selected bar
        expect(momondoHomepage.getSelectedBarStatus(newSelectGraphBar)).toContain('selected');
    });
    // 2)
    it('Should display Price of selected bar',async function () {
        const selectedBarStatus = await momondoHomepage.getSelectedBarPrice();
        expect(selectedBarStatus).toEqual(true);
    });
    // 3)
    it('Should display ‘Price shown are estimates per person”',function () {
        const selectedPriceTextShownStatus = momondoHomepage.getSelectedPriceTextShown();
        expect(selectedPriceTextShownStatus).toEqual(true);
    });
    // 4)
    it('Should display ‘Search these days’ button',function () {
        const searchBtnShown = momondoHomepage.getSearchBtnShown();
        expect(searchBtnShown).toEqual(true);
    });



    // Step 6

    // 1)
    it('Should display updated date in first result’s details section',async function () {
        momondoHomepage.searchTheseDays();
        momondoHomepage.showDetails();
        const FirstResultDepartureDate = momondoHomepage.getDepartureDateInDetailsPanel();
        // Should match the departure date in first result card i.e. Tue, Aug 10 with selected date in the bar graph i.e YYYY-MM-DD
        const expectedDate = moment(SELECTED_DATE).format('ddd, MMM D');
        expect(FirstResultDepartureDate.getText()).toEqual(expectedDate);
    });
    // 2)
    it('Should display updated departure date',function () {
        const departureField = momondoHomepage.getDepartureDate();
        // Should match the departure date in search form i.e. Tue M/D with selected date in the bar graph i.e YYYY-MM-DD
        const expectedDate = moment(SELECTED_DATE).format('ddd M/D');
        expect(departureField.getText()).toBe(expectedDate);
    });
    // 3)
    it('Should not display ‘Price shown are estimates per person’ label',async function () {
        const estimatesPerPersonText = await momondoHomepage.isSelectedPriceTextShownExist();
        expect(estimatesPerPersonText).toEqual(false);
    });
    // 4)
    it('Should not display ‘Search these days’ button',async function () {
        const searchTheseDaysButton = await momondoHomepage.isSearchTheseDaysButtonExist();
        // Should display ‘Search these days’ button
        expect(searchTheseDaysButton).toEqual(false);
    })

});
