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

    it('should display hotel reviews and rates: Step 5-6', function () {

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

            var hotel = results.first();

            hotel.click().then(function () {

                var detailsCon = element.all(by.css("[id*=detailsWrapper]")).first();
                browser.wait(EC.visibilityOf(detailsCon), 6000);

                expect((detailsCon).isPresent()).toBe(true);

                //Step 5: check the reviews in review tab

                var reviewTab = detailsCon.all(by.css("[id*=reviews]")).first();
                browser.wait(EC.visibilityOf(reviewTab), 7500);

                expect((reviewTab).isPresent()).toBe(true);

                reviewTab.click().then(function () {

                    var reviewContainer = element.all(by.css("[id*=reviewsContainer]")).first();
                    browser.wait(EC.visibilityOf(reviewContainer), 3000);

                    expect((reviewContainer).isPresent()).toBe(true);

                });

                //Step 6: check the rates in rate tab

                var ratesTab = detailsCon.all(by.css("[id*=rates]")).first();
                browser.wait(EC.visibilityOf(ratesTab), 6000);

                expect((ratesTab).isPresent()).toBe(true);

                ratesTab.click().then(function () {

                    var ratesContainer = element.all(by.css("[id*=ratesContainer]")).first();
                    browser.wait(EC.visibilityOf(ratesContainer), 4000);

                    expect((ratesContainer).isPresent()).toBe(true);

                });

            });

        });

    });

});
