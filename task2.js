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

    it('should set BCN and search hotels: Step 2', function () {

        openLink(browser.params.hotels);

        var originField = element.all(by.css("[id *= location-display]")).first().click()
        browser.wait(EC.visibilityOf(originField), 7000);
        //set the origin

        var originText = element.all(by.css("[id *= textInputWrapper]")).first().element(by.tagName('input'));
        browser.wait(EC.visibilityOf(originText), 7000);
        originText.sendKeys(browser.params.bcnKeys);

        //select the origin

        var originList = element.all(by.css("[id *= location-smarty-content]")).first();

        expect((originList).isPresent()).toBe(true);

        browser.wait(EC.elementToBeClickable(originList), 5000);

        originList.all(by.tagName('li')).first().click();

        //press the search button

        var searchBtn = element(by.css("[id$=-formGridSearchBtn]")).element(by.tagName('button'));
        searchBtn.click().then(function () {

            // check the result set
            var resultsContainer = element(by.css("[id = searchResultsList]"));
            browser.wait(EC.presenceOf(resultsContainer), 10000);

            var resultbox = element(by.css("[class *= normalResults]"));
            browser.wait(EC.presenceOf(resultbox), 10000);



            var results = resultsContainer.all(by.css("[class*=Base-Results-HorizonResult]"));
            browser.wait(EC.presenceOf(results), 10000);

            var resultCount = results.count();

            expect(resultCount).toBeGreaterThanOrEqual(5);
        });

    });

});
