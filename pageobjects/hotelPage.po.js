var utils = require('./../utils/common');

var HotelPage = function() {
    
    this.getHotelPageInfo = function() {
        return {
            singleHotelClass: ".resultWrapper",
            originDropdownSelector: "div[id$=-location-smartbox-dropdown]",
            searchResultSelector: "div[id=searchResultsList]",
            mapContentSelector: ".Hotels-Results-InlineTab.Hotels-Results-InlineMap",
            reviewSelector: ".Hotels-Results-InlineTab.Hotels-Results-InlineReviews",
            ratesSelector: ".Hotels-Results-InlineTab.Hotels-Results-InlineRates",
            goToMapSelector: ".Hotels-Results-HotelRightRailMap.open"
        };
    };

    this.getHotelSearchResult = function() {
        return element.all(by.css(this.getHotelPageInfo().singleHotelClass));
    };

    this.waitForSearchCompletion = function() {
        var EC = protractor.ExpectedConditions;
        browser.wait(EC.visibilityOf(element(by.css('.resultsContainer')).element(by.css('.finished'))), 10000, 'Error! Unable to load hotels list in selected origin');
    };

    this.getFirstHotelFromList = function() {
        return this.getHotelSearchResult().first();
    };

    this.getFirstHotelDetail = function() {
        return element.all(by.css(this.getHotelPageInfo().searchResultSelector))
            .first()
            .all(by.css(this.getHotelPageInfo().singleHotelClass))
            .first()
            .all(by.css('.Hotels-Results-InlineDetailTabs'));
    };

    this.getFirstHotelTitle = function() {
        return this.getFirstHotelFromList().all(by.css('button[id$=info-title]'));
    };

    this.getFirstHotelPhotos = function() {
        try {
            const firstHotelInfo = this.getFirstHotelDetail();
            if(firstHotelInfo.isPresent()) {
                return firstHotelInfo.first().all(by.css('.photoGrid')).first().all(by.css('.col-1-3'));
            }
        }
        catch(err) {
            utils.handleException('getFirstHotelPhotos'. err.message);
        }
    };

    this.getFirstHotelTab = function(tabName) {
        try {
            let tabId = '';
            if(tabName === 'map') {
                tabId = 'map'
            } 
            else if (tabName === 'review') {
                tabId = 'reviews';
            }
            else if (tabName === 'rates') {
                tabId = 'rates'
            }
            const tabSelector = `div[id$=-${tabId}]`;
            const result = this.getFirstHotelDetail()
                .first()
                .all(by.css("div[id$=-tabs]"))
                .first()
                .all(by.css(tabSelector))
                .first();

            return result;
        }
        catch(err) {
            utils.handleException('getFirstHotelTab'. err.message);
        }
        return null;
    };

    this.getGoToMap = function() {
        const goToMap = element(by.css('.collapsible-wrapper')).element(by.css('div[id$=-map]'));
        return goToMap;
    }

    this.getHotelMarkers = function() {
        return element.all(by.css('.hotel-marker'));
    }

    this.getSingleHotelMarkers = function(elements, index) {
        const hotelMarker = elements.get(index);
        hotelMarker.getText().then(function(txt){
            console.log(`title of hotel marker hovered: ${txt}`);
        });
        return hotelMarker;
    }

    this.getVisibleHotelMarker = function(hotelMarkers, index) {
        hotelMarker = hotelMarkers.get(index);
        hotelMarker.getLocation().then(function(location) {
            console.log('location', location.y);
            if(location.y > 0) {
                return hotelMarker;
            }
        });
    }

    this.getAllHotelMarkers = function() {
        return element.all(by.css('.hotel-marker'));
    }

    this.getSingleHotelMarker = function(hotelMarkers, index) {
        return hotelMarkers.get(index);
    }

    
    this.verifyHotelMarker = function() {
        // get all hover markers
        const hotelMarkers = this.getAllHotelMarkers();

        hotelMarkers.count().then(totalMarkers => {
            console.log(`total hotel markers found: ${totalMarkers}`);

            // get single hover marker
            hotelMarker = this.getSingleHotelMarker(hotelMarkers, 0);
            hotelMarker.getCssValue('top').then(function(location) {
                console.log('location x || y', location);

                 // move mouse over hotel marker
                browser.actions().mouseMove(hotelMarker).perform().then(function() {
                    browser.sleep(2000);
                    hotelMarker.getText().then(function(txt) {
                    console.log('title of hotel marker hovered:', txt);
                    });

                    // get hovered hotel marker id
                    hotelMarker.getAttribute("id").then(function(value) {
                        if(value) {

                            // verify hover box is visible
                            const id = value.replace(/^\D+/g, '');
                            const hoverBoxId = `summaryCard-${id}`;
                            console.log('hover box id', hoverBoxId);
                            
                            const hoveredBox = element(by.css(`div[id=${hoverBoxId}]`));
                            hoveredBox.getText().then(function(value) {
                                console.log('hovered element text: ', value);
                                
                                // click hovered box
                                hoveredBox.click().then(function() {
                                    browser.sleep(10000);
                                    const hotelDetailWrapperId = "div[id='"+id+"-photo']";
                                    const selectedHotelImage = element(by.css(hotelDetailWrapperId));

                                    // verify hotel image is present on top left
                                    expect(selectedHotelImage.isPresent()).toBe(true);
                                    /* selectedHotelImage.getText().then(function(value) {
                                        
                                    }); */

                                    // click view deal button
                                    const viewDetailBtn = `button[id='${id}-booking-bookButton']`;
                                    element(by.css(viewDetailBtn)).click().then(function() {
                                        console.log("view deal button clicked");
                                        browser.sleep(3000);
                                        browser.getAllWindowHandles().then(function(handles) {
                                            browser.switchTo().window(handles[1]).then(function(){
                                                browser.getCurrentUrl().then(function(url) {
                                                    console.log('opened deal page url: ', url);
                                                    expect(url && url.length > 0).toBe(true);
                                                });
                                            }); // end >> browser switchTo
                                        }); // end >> getAllWindowHandles()
                                    }); // end >> Click view detail buton
                                }); // end >> hovered box clicked
                            }); // end >> hovered box >> getText() 
                        }
                        else {
                            console.log('hotel marker not found');
                        }
                    }); // end >> get id of hovered hotel marker 
                }); // end >> move mouse over hotel marker
            }); // end >> get selected hotel marker "top" location 
        }); // end >> get hotel markers count
    }
};

module.exports = HotelPage;