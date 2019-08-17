describe('kayak website', function () {
    beforeEach(function () {
        browser.waitForAngularEnabled(false);
        browser.get(browser.params.kayakSiteLink);
        global.EC = protractor.ExpectedConditions;

    });

    function openLink(link) {
        var link = element(by.linkText(link));
        browser.wait(EC.visibilityOf(link), 15000);
        link.click();
    }

    it('should display selected hotle details and provider page: Step 9-10', function () {

        openLink(browser.params.hotels);

        var originField = element.all(by.css("[id *= location-display]")).first().click()
        browser.wait(EC.visibilityOf(originField), 7000);
        
        var originText = element.all(by.css("[id *= textInputWrapper]")).first().element(by.tagName('input'));
        browser.wait(EC.visibilityOf(originText), 7000);
        originText.sendKeys(browser.params.bcnKeys);
        
        var originList = element.all(by.css("[id *= location-smarty-content]")).first();

        expect((originList).isPresent()).toBe(true);

        browser.wait(EC.elementToBeClickable(originList), 5000);

        originList.all(by.tagName('li')).first().click();

        var searchBtn = element(by.css("[id$=-formGridSearchBtn]")).element(by.tagName('button'));
        searchBtn.click().then(function () {

            var resultsContainer = element(by.css("[id = searchResultsList]"));
            browser.wait(EC.presenceOf(resultsContainer), 10000);

            var resultbox = element(by.css("[class *= normalResults]"));
            browser.wait(EC.presenceOf(resultbox), 10000);

            var results = resultsContainer.all(by.css("[class*=Base-Results-HorizonResult]"));
            browser.wait(EC.presenceOf(results), 10000);


            var mapView = element.all(by.css("[class *= filterListContainer]")).first();

            expect((mapView).isPresent()).toBe(true);
            var mapBtn = mapView.element(by.css(".showMap"));
            expect((mapBtn).isPresent()).toBe(true);
            mapBtn.click().then(function () {
                
                var mapContainer = element.all(by.css("[class *= rail-map-container")).first();
                browser.wait(EC.elementToBeClickable(mapContainer), 10000);
                expect((mapContainer).isPresent()).toBe(true);

                //Step 8: mouse hover the hotel markers

                browser.wait(EC.visibilityOf(mapContainer.element(by.css(".gm-style"))), 15000);
                var hotelMarker = mapContainer.all(by.css(".hotel-marker"));
                var selectedHotel = hotelMarker.first();

                hotelMarker.each(function (elem, index) {

                    elem.getCssValue("top").then(function (top) {

                        if (top > 0) {
                            selectedHotel = element;
                            expect((selectedHotel).isPresent()).toBe(true);
                            browser.actions().mouseMove(selectedHotel).mouseMove(selectedHotel).perform().then(function () {

                                var hotelId = selectedHotel.getAttribute("id").then(function (value) {

                                    var id = value.substring(value.indexOf('-'), value.length);
                                    var cardId = 'summaryCard' + id;

                                    var summaryCard = element(by.css("[id *= " + cardId + "]"));

                                    expect((summaryCard).isDisplayed()).toBeTruthy();

                                });

                            });
                        }

                    });
                });


                //Step 9: click the deal btn

                browser.actions().mouseMove(selectedHotel).mouseMove(selectedHotel).click().perform().then(function () {
                    var resultWrapper = element.all(by.css("[class *= resultWrapper]")).first();
                    browser.wait(EC.visibilityOf(resultWrapper), 10000);

                    var itemWrapper = resultWrapper.all(by.css("[id *= mainItemWrapper]")).first();
                    browser.wait(EC.visibilityOf(itemWrapper), 10000);

                    var dealBtn = element.all(by.css("[id *= bookButton]")).first();
                    dealBtn.click().then(function () {

                        // Step 10: check the deals in new tab
                        browser.getAllWindowHandles().then(function (handles) {
                            newWindowHandle = handles[1]; // this is your new window
                            browser.switchTo().window(newWindowHandle).then(function () {
                                browser.wait(function () {
                                    expect(browser.getCurrentUrl()).toContain("https://www.hotels.com/"); //someURL
                                });
                            });
                        });
                    });
                });
            });
        });
    });
});
