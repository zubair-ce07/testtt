// testcases.js
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


    it('should check the link title and fields: Step 1', function () {

        openLink(browser.params.hotels);

        expect(browser.getTitle()).toEqual(browser.params.hotleLinkTitle);

        var guestField = element(by.css("[id *= roomsGuestsAboveForm]")).element(by.css("[class *= _idj]"));

        expect(guestField.getText()).toBe(browser.params.guestFieldText);

        var originField = element(by.css("[id *= location-textInputWrapper]"));

        expect((originField).isPresent()).toBe(true);

        var startDateField = element(by.css("[id *= dateRangeInput-display-start]"));

        expect((startDateField).isPresent()).toBe(true);

        var endDateField = element(by.css("[id *= dateRangeInput-display-end]"));

        expect((endDateField).isPresent()).toBe(true);
    });


});
