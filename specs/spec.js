let homePageObject = require('./../pageobjects/homePage.po.js');
let hotelPageObject = require('./../pageobjects/hotelPage.po');
let utils = require('./../utils/common.js');

describe('Hostel App', function() {

    let homePage = new homePageObject();
    let hotelPage = new hotelPageObject();
    
    it("Should display the origin on home page", function() {
        // open hotels page
        homePage.getHotelsPage();
        expect(browser.getCurrentUrl()).toEqual(homePage.getHomePageInfo().hotelPageUrl);

        expect(homePage.getOriginField().isDisplayed()).toBe(true);
    });

    it("Should display the start date on home page", function() {
        const {startDate } = homePage.getDateFields();
        expect(startDate.isDisplayed()).toBe(true);
    });

    it("Should display the end date on home page", function() {
        const {endDate } = homePage.getDateFields();
        expect(endDate.isDisplayed()).toBe(true);
    });

    it("Should display ‘1 room, 2 guests’ in guests field", function() {
        expect(homePage.getGuestField().getText()).toEqual(homePage.getHomePageInfo().guestFieldText);
    });

    it("Should load hotels results page", function() {
        homePage.searchOriginsList();
        hotelPage.waitForOriginsListPresence();
        homePage.selectFirstOriginFromList();
        
    });

    it("Should display at least 5 hotel results", async function() {
        // click search button on home page
        const searchBtn = hotelPage.getSearchButton();
        await searchBtn.click()
        hotelPage.waitForSearchCompletion();

        // verify atleast 5 hotels should display in search result
        const searchResult = hotelPage.getHotelSearchResult();
        const hotelsCount = await searchResult.count();
        console.log(`total hotels found: ${hotelsCount}`);
        expect(hotelsCount).toBeGreaterThan(4);
    })
 
    it("should verify hotel detail page", function() {
        let hotelsList = hotelPage.getHotelSearchResult();
        if(hotelsList)
        {
            // click hotel title
            const titleLink = hotelPage.getFirstHotelTitle();
            titleLink.click().then(function() {
                titleLink.getText().then(function(value) {
                    console.log(`hotel title clicked: "${value}"`);
                })
                browser.sleep(5000).then(function() {
                    utils.waitForElementPresence(hotelPage.getHotelPageInfo().singleHotelClass, 10000, 'Error! Unable to load hotels in selected origin');

                    // verify selected hotel detail page
                    const hostelDetail = hotelPage.getFirstHotelDetail();
                    expect(hostelDetail.isPresent()).toBe(true);
    
                    // verify selected hotel photos count
                    const photosCount = hotelPage.getFirstHotelPhotos().count();
                    expect(photosCount).toBeGreaterThan(0);
                    photosCount.then(function(value) {
                        console.log(`hotel photos count: ${value}`);
                    });
                });
            });
        }
    });

     it("should verify map section in hotel detail", function() {
        const hotelMap = hotelPage.getFirstHotelTab('map');

        hotelMap.getAttribute("id").then(function(hotelMapId) {
            element(by.css(`div[id=${hotelMapId}]`))
                .click()
                .then(function() {
                    console.log("map tab is clicked");
                    const mapContent = element.all(by.css(hotelPage.getHotelPageInfo().singleHotelClass))
                    .first()
                    .all(by.css(hotelPage.getHotelPageInfo().mapContentSelector));   
                    browser.sleep(10000).then(function() {
                        mapContent.count().then(function(value) {
                            expect(value).toBe(1);
                            //expect(getFirstHotelMapContent().isPresent()).toBe(true);
                        });
                    });
                });
        });
    });

    it("should verify reviews section in hotel detail", function() {
        const hotelReview = hotelPage.getFirstHotelTab('review');

        hotelReview.getAttribute("id").then(function(id) {
            element(by.css(`div[id=${id}]`))
                .click()
                .then(function() {
                    console.log("review tab is clicked");
                    const reviewContent = element.all(by.css(hotelPage.getHotelPageInfo().singleHotelClass))
                    .first()
                    .all(by.css(hotelPage.getHotelPageInfo().reviewSelector));
                    browser.sleep(2000).then(function() {
                        expect(reviewContent.isPresent()).toBe(true);
                    });
                });
        });
    });


    it("should verify rates section in hotel detail", function() {
        const hotelReview = hotelPage.getFirstHotelTab('rates');

        hotelReview.getAttribute("id").then(function(id) {
            element(by.css(`div[id=${id}]`))
                .click()
                .then(function() {
                    console.log("rates tab is clicked");
                    const ratesContent = element.all(by.css(hotelPage.getHotelPageInfo().singleHotelClass))
                    .first()
                    .all(by.css(hotelPage.getHotelPageInfo().ratesSelector));
                    browser.sleep(2000).then(function() {
                        expect(ratesContent.isPresent()).toBe(true);
                    });
                });
        });
    }); 

    it("should verify GO To Map button, hotel marker hover, hover marker image and deal button", function() {
        const goToMap = hotelPage.getGoToMap();
        goToMap.getText().then(function(value) {
            console.log('go to map button clicked');
            goToMap.click().then(function() {
                browser.sleep(10000).then(function() {
                    const mapContent = element(by.css(hotelPage.getHotelPageInfo().goToMapSelector));
                    expect(mapContent.isPresent()).toBe(true);
                    hotelPage.verifyHotelMarker();
                });
                
            });
        });
    });

});