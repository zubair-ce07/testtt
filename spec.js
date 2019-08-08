const moment = require('moment');
const momondoHomepage = require('./pages/homePage');
describe('Protractor Demo App', function() {
    // To ignore checking the angular app
    browser.ignoreSynchronization = true;
    let SELECTED_DATE = '';
    momondoHomepage.get();
    // Step 1
    // 1)
    it('Should display ‘London (LON)’ in the origin field', function() {
        expect(momondoHomepage.getOriginFieldText()).toEqual('London (LON)');
    });
    // 2)
    it('Should display ‘New York (NYC)’ in the destination field.', function() {
        expect(momondoHomepage.getDestinationFieldText()).toEqual('New York (NYC)');
    });
    // 3)
    it('Should display ‘Sat 8/10’ in the departure date field', function() {
        expect(momondoHomepage.getDepartureFieldText()).toBe('Sat 8/10');
    });
    // 4)
    it('Should display ‘Tue 9/10’ in the return date field.', function() {
        expect(momondoHomepage.getReturnFieldText()).toBe('Tue 9/10');
    });
    // 5)
    it('Should display ‘1 Adult, Economy’ in travelers field', function() {
        expect(momondoHomepage.getTravelersFieldText()).toBe('1 Adult, Economy');
    });
    // 6)
    it('Should display ‘Estimated Price Graph’ below the search form', function() {
       expect(momondoHomepage.isGraphVisible()).toEqual(true);
    });


    // Step 2

    it('Should display first half of estimated price graph',async function () {
        // get oneway radio button
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
        // browser.sleep(5000);
        momondoHomepage.showDetails();
        let departureDateValue = momondoHomepage.getDepartureDateInDetailsPanel();
        let tempDate = moment(SELECTED_DATE).format('ddd, MMM D');
        expect(departureDateValue.getText()).toEqual(tempDate);
    });
    // // 2)
    // it('Should display updated departure date',function () {
    //     let departField = element(by.xpath("//div[contains(@id,'-dateRangeInput-display-start-inner')]"));
    //     let tempDate = moment(SELECTED_DATE).format('ddd M/D');
    //     expect(departField.getText()).toBe(tempDate);
    // });
    // // 3)
    // it('Should not display ‘Price shown are estimates per person’ label',function () {
    //     let estimatesPerPersonText = element(by.className('hightlight'));
    //     // Should display ‘Price shown are estimates per person”
    //     estimatesPerPersonText.isPresent().then(function (value) {
    //         expect(value).toEqual(false);
    //     });
    // });
    // // 4)
    // it('Should not display ‘Search these days’ button',function () {
    //     let searchTheseDaysButton = element(by.xpath("//a[contains(@aria-describedby,'-search-dates-description')]"));
    //     // Should display ‘Search these days’ button
    //     searchTheseDaysButton.isPresent().then(function (value) {
    //         expect(value).toEqual(false);
    //     });
    // })

});
