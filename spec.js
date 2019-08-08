var moment = require('moment');
describe('Protractor Demo App', function() {
    // To ignore checking the angular app
    browser.ignoreSynchronization = true;
    browser.get('https://global.momondo.com/flight-search/LON-NYC/2019-08-10/2019-09-10?sort=price_a');
    let SELECTED_DATE = '';
    let EC = protractor.ExpectedConditions;
    // beforeEach(function() {
    //     browser.get('https://global.momondo.com/flight-search/LON-NYC/2019-08-10/2019-09-10?sort=price_a');
    //     // browser.sleep(5000);
    // });
    // Step 1
    // 1)
    it('shoould have a origin set to `London (LON)`', function() {
        expect(element(by.name('origin')).getAttribute('value')).toEqual('London (LON)');
    });
    // 2)
    it('shoould have a destination set to `‘New York (NYC)`', function() {
        expect(element(by.name('destination')).getAttribute('value')).toEqual('New York (NYC)');
    });
    // 3)
    it('Should display ‘Sat 8/10’ in the departure date field', function() {
        // Searching depart field based on the data-placeholder because everytime page refreshes its ID is changed.
        let departField = element(by.xpath("//div[contains(@id,'-dateRangeInput-display-start-inner')]"));
        expect(departField.getText()).toBe('Sat 8/10');
    });
    // 4)
    it('Should display ‘Tue 9/10’ in the return date field.', function() {
        // Searching depart field based on the data-placeholder because everytime page refreshes its ID is changed.
        let returnField = element(by.xpath("//div[contains(@id,'-dateRangeInput-display-end-inner')]"));
        expect(returnField.getText()).toBe('Tue 9/10');
    });
    // 5)
    it('Should display ‘1 Adult, Economy’ in travelers field', function() {
        // Searching depart field based on the data-placeholder because everytime page refreshes its ID is changed.
        // /div[@class='col-travelers']/div/a/div[@class='label']
        let travelersField = element(by.xpath("//a[contains(@id, '-travelers-dialog')]/div[contains(@class,label)]"));
        expect(travelersField.getText()).toBe('1 Adult, Economy');
    });
    // 6)
    it('Should display the graph', function() {
        // Searching depart field based on the data-placeholder because everytime page refreshes its ID is changed.
        // /div[@class='col-travelers']/div/a/div[@class='label']
        let graphElement = element(by.className('graph-grid'));
        browser.wait(EC.visibilityOf(graphElement),5000);
        graphElement.isPresent().then(function (value) {
           expect(value).toEqual(true);
        });
    });


    // Step 2

    it('Should display first half of estimated price graph',async function () {
        console.log('Step 2');
        // get oneway radio button
        await element(by.css("label[title=One-way]")).click();
        await element(by.css("button[aria-label='Edit search']")).click();
        browser.sleep(5000);
        let elements = $$('.graph-col');
        expect(elements.count()).toEqual(1);
    });


    // Step 3

    it('Should display both graphs',async function () {
        // console.log('Step 3');
        // get oneway radio button
        await element(by.css("label[title=Round-trip]")).click();
        // browser.sleep(10000);
        await element(by.xpath("//div[contains(@id,'-dateRangeInput-display-end-inner')]")).click();
        // browser.sleep(1000);
        let calendarDate = element(by.css("div[aria-label='September 10']"));
        // Wait for the calendar to be visible
        browser.wait(EC.elementToBeClickable(calendarDate), 5000);
        calendarDate.click();
        // Wait for the Calendar to hide
        browser.wait(EC.not(EC.visibilityOf(calendarDate)),5000);
        await element(by.css("button[aria-label='Edit search']")).click();
        browser.sleep(3000);
        let elements = $$('.graph-col');
        expect(elements.count()).toEqual(2);
    });

    // Step 4

    it('Should display tooltip with price',function () {
        // browser.sleep(3000);
        let hoverElement = element(by.css("button[data-date='2019-08-11']"));
        browser.actions().mouseMove(hoverElement).perform();
        let childElement = hoverElement.element(by.css('.bar')).element(by.css('.price-info')).element(by.css('.price-price'));
        expect(childElement.getText()).toContain('USD');
        // browser.sleep(3000);
    });

    // Step 5
    // 1)
    it('Should highlight selected bar',function () {
        let selectedBar = element(by.css('.Button-No-Standard-Style.js-bar.item.selected'));
        // Wait for the selected bar to be visible
        browser.wait(EC.elementToBeClickable(selectedBar), 5000);
        let pre_selectedDate = browser.wait(function () {
            // Getting the pre-selected date
            return selectedBar.getAttribute('data-date').then(function (value) {
                let newDate = moment(value).add(2,'days').format('YYYY-MM-DD');
                console.log(newDate);
                return newDate;
            })
        });
        pre_selectedDate.then( async function (value) {
            // Saving this value variable which is the selected date in a global variable to use in later test cases
            SELECTED_DATE = value;
            let newSelectElement = element(by.css("button[data-date='"+value+"']"));
            await newSelectElement.click();
            browser.sleep(2000);
            expect(newSelectElement.getAttribute('class')).toContain('selected');
            // Getting elements
            let selectedPrice = element(by.className('highlight-price'));
            let estimatesPerPersonText = element(by.className('hightlight'));
            let searchTheseDaysButton = element(by.xpath("//a[contains(@aria-describedby,'-search-dates-description')]"));
            // Should display Price of selected bar
            selectedPrice.isPresent().then(function (value) {
                expect(value).toEqual(true);
            });
            // Should display ‘Price shown are estimates per person”
            estimatesPerPersonText.isPresent().then(function (value) {
                expect(value).toEqual(true);
            });
            // Should display ‘Search these days’ button
            searchTheseDaysButton.isPresent().then(function (value) {
                expect(value).toEqual(true);
            });
        })
    });
    // 6)
    it('Should display updated date in first result’s details section',async function () {
        let searchTheseDaysButton = element(by.xpath("//a[contains(@aria-describedby,'-search-dates-description')]"));
        await searchTheseDaysButton.click();
        browser.sleep(5000);
        let firstCardSearchBtn = element.all(by.xpath("//div[contains(@id,'-extra-info-details-link')]")).first();
        await  firstCardSearchBtn.click();
        browser.sleep(5000);
        let detailsPanelDepartureDate = element.all(by.css('.leg-dates-set')).first();
        let departureDateValue = detailsPanelDepartureDate.element(by.css('div'));
        // console.log(departureDateValue);
        let tempDate = moment(SELECTED_DATE).format('ddd, MMM D');
        // console.log(new Date(tempDate[0],tempDate[1] - 1, tempDate[2]));
        // console.log(tempDate);
        expect(departureDateValue.getText()).toEqual(tempDate);
    });
    // 2)
    it('Should display updated departure date',function () {
        let departField = element(by.xpath("//div[contains(@id,'-dateRangeInput-display-start-inner')]"));
        let tempDate = moment(SELECTED_DATE).format('ddd M/D');
        expect(departField.getText()).toBe(tempDate);
    });
    // 3)
    it('Should not display ‘Price shown are estimates per person’ label',function () {
        let estimatesPerPersonText = element(by.className('hightlight'));
        // Should display ‘Price shown are estimates per person”
        estimatesPerPersonText.isPresent().then(function (value) {
            expect(value).toEqual(false);
        });
    });
    // 4)
    it('Should not display ‘Search these days’ button',function () {
        let searchTheseDaysButton = element(by.xpath("//a[contains(@aria-describedby,'-search-dates-description')]"));
        // Should display ‘Search these days’ button
        searchTheseDaysButton.isPresent().then(function (value) {
            expect(value).toEqual(false);
        });
    })

});
