var homePage = require('./../pageobjects/homePage.po.js');
var hotelPage = require('./../pageobjects/hotelPage.po');
var utils = require('./../utils/common.js');

describe('Hostel App', function() {

    var home = new homePage();
    var hotel = new hotelPage();

    it("1. should verify origin, start date, end date and guest field on home page", function() {
        // open hotels page
        home.getHotelsPage();
        expect(browser.getCurrentUrl()).toEqual(home.getHomePageInfo().hotelPageUrl);

        // verify origin field
        expect(home.getOriginField().isPresent()).toBe(true);

        // verify start & end date field
        const {startDate, endDate } = home.getDateFields();
        expect(startDate.isPresent()).toBe(true);
        expect(endDate.isPresent()).toBe(true);

        // verify guest field
        expect(home.getGuestField().getText()).toEqual(home.getHomePageInfo().guestFieldText);
    });

    it("2. should verify hotel page search", function() {
        // set keywork like 'BCN in origin field
        home.searchOriginsList(home.getHomePageInfo().originSearchKeywork);
        const originDDSelector = hotel.getHotelPageInfo().originDropdownSelector;
        utils.waitForElementPresence(originDDSelector, 10000, 'Error! Unable to load hotel result page');
        home.selectFirstOriginFromList();

        // click search button on home page
        const searchBtn = element(by.css(home.getHomePageInfo().searchBtnSelector));
        searchBtn.click().then(function(result){

            browser.sleep(5000).then(function() {

                // 
                //utils.waitForElementVisibility(hotel.getHotelPageInfo().searchResultSelector, 10000, 'Error! Unable to load hotels list in selected origin');
                //var EC = protractor.ExpectedConditions;
                //browser.wait(EC.visibilityOf(element(by.css('.resultsContainer')).element(by.css('.finished'))), timeout, error);

                hotel.waitForSearchCompletion();
                utils.waitForElementPresence(hotel.getHotelPageInfo().singleHotelClass, 10000, 'Error! Unable to load hotels in selected origin');
    
                // verify atleast 5 hotels should display in search result
                const searchResult = hotel.getHotelSearchResult();
                searchResult.count().then(function(value) {
                    console.log(`total hotels found: ${value} `);
                    const searchResultDiv = element(by.css(hotel.getHotelPageInfo().searchResultSelector));
                    expect(searchResultDiv.isPresent()).toBe(true);
                    /* searchResultDiv.getText().then(function(value) {
                      expect(searchResultDiv.isPresent()).toBe(true);
                    }); */
    
                    expect(value).toBeGreaterThan(4);
                });
            });
        });
    });

    it("3. should verify hotel detail page", function() {
        let hotelsList = hotel.getHotelSearchResult();
        if(hotelsList)
        {
            // click hotel title
            const titleLink = hotel.getFirstHotelTitle();
            titleLink.click().then(function() {
                titleLink.getText().then(function(value) {
                    console.log(`hotel title clicked: "${value}"`);
                })
                browser.sleep(5000).then(function() {
                    utils.waitForElementPresence(hotel.getHotelPageInfo().singleHotelClass, 10000, 'Error! Unable to load hotels in selected origin');

                    // verify selected hotel detail page
                    const hostelDetail = hotel.getFirstHotelDetail();
                    expect(hostelDetail.isPresent()).toBe(true);
    
                    // verify selected hotel photos count
                    const photosCount = hotel.getFirstHotelPhotos().count();
                    expect(photosCount).toBeGreaterThan(0);
                    photosCount.then(function(value) {
                        console.log(`hotel photos count: ${value}`);
                    });
                });
            });
        }
    });

     it("4. should verify map section in hotel detail", function() {
        const hotelMap = hotel.getFirstHotelTab('map');

        hotelMap.getAttribute("id").then(function(hotelMapId) {
            element(by.css(`div[id=${hotelMapId}]`))
                .click()
                .then(function() {
                    console.log("map tab is clicked");
                    const mapContent = element.all(by.css(hotel.getHotelPageInfo().singleHotelClass))
                    .first()
                    .all(by.css(hotel.getHotelPageInfo().mapContentSelector));   
                    browser.sleep(10000).then(function() {
                        mapContent.count().then(function(value) {
                            expect(value).toBe(1);
                            //expect(getFirstHotelMapContent().isPresent()).toBe(true);
                        });
                    });
                });
        });
    });

    it("5. should verify reviews section in hotel detail", function() {
        const hotelReview = hotel.getFirstHotelTab('review');

        hotelReview.getAttribute("id").then(function(id) {
            element(by.css(`div[id=${id}]`))
                .click()
                .then(function() {
                    console.log("review tab is clicked");
                    const reviewContent = element.all(by.css(hotel.getHotelPageInfo().singleHotelClass))
                    .first()
                    .all(by.css(hotel.getHotelPageInfo().reviewSelector));
                    browser.sleep(2000).then(function() {
                        expect(reviewContent.isPresent()).toBe(true);
                    });
                });
        });
    });


    it("6. should verify rates section in hotel detail", function() {
        const hotelReview = hotel.getFirstHotelTab('rates');

        hotelReview.getAttribute("id").then(function(id) {
            element(by.css(`div[id=${id}]`))
                .click()
                .then(function() {
                    console.log("rates tab is clicked");
                    const ratesContent = element.all(by.css(hotel.getHotelPageInfo().singleHotelClass))
                    .first()
                    .all(by.css(hotel.getHotelPageInfo().ratesSelector));
                    browser.sleep(2000).then(function() {
                        expect(ratesContent.isPresent()).toBe(true);
                    });
                });
        });
    });

    it("7. should verify GO To Map button on hotel detail page", function() {
        const goToMap = hotel.getGoToMap();
        goToMap.getText().then(function(value) {
            console.log('go to map button clicked');
            goToMap.click().then(function() {
                browser.sleep(10000).then(function() {
                    const mapContent = element(by.css(hotel.getHotelPageInfo().goToMapSelector));
                    expect(mapContent.isPresent()).toBe(true);
                });
                
            });
        });
    });

});