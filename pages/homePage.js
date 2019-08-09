const moment = require('moment');
const homePage = function () {
    browser.ignoreSynchronization = true;
    const EC = protractor.ExpectedConditions;
    this.get = async function() {
        await browser.get('https://global.momondo.com/flight-search/LON-NYC/2019-08-10/2019-09-10?sort=price_a');
    };
    this.getOriginFieldText = function () {
        return element(by.name('origin')).getAttribute('value');
    };
    this.getDestinationFieldText = function () {
        return element(by.name('destination')).getAttribute('value');
    };
    this.getDepartureFieldText = function () {
        return element(by.xpath("//div[contains(@id,'-dateRangeInput-display-start-inner')]")).getText();
    };
    this.getReturnFieldText = function () {
        return element(by.xpath("//div[contains(@id,'-dateRangeInput-display-end-inner')]")).getText();
    };
    this.getTravelersFieldText = function () {
        return element(by.xpath("//a[contains(@id, '-travelers-dialog')]/div[contains(@class,label)]")).getText();
    };
    this.isGraphVisible = function () {
        let graphElement = element(by.css('.graph-grid'));
        browser.wait(EC.visibilityOf(graphElement),5000);
        return graphElement.isPresent();
    };
    this.selectTripType = function (tripType) {
        element(by.css("label[title='"+tripType+"']")).click();
    };
    this.getMainVisibleGraphCount = function (operationType) {
        element(by.css("button[aria-label='Edit search']")).click();
        let graphElement = element.all(by.css('.graph-col'));
        if(operationType === 'first_half') {
            // Waiting for the second graph to be invisible
            browser.wait(EC.invisibilityOf(graphElement.get(1)),5000);
        } else {
            // Waiting for the second graph to be visible
            browser.wait(EC.visibilityOf(graphElement.get(1)),5000);
        }
        graphElement = element.all(by.css('.graph-col'));
        return graphElement.count();
    };
    this.selectDateFromCalendar = function () {
        element(by.xpath("//div[contains(@id,'-dateRangeInput-display-end-inner')]")).click();
        const newcalendarDate = element(by.css("div[aria-label='September 10']"));
        // Wait for the calendar to be visible
        browser.wait(EC.elementToBeClickable(newcalendarDate), 5000);
        newcalendarDate.click();
        // Wait for the Calendar to hide
        browser.wait(EC.invisibilityOf(newcalendarDate), 5000);
    };
    this.hoverOverGraphBar = function () {
        const grapBar = element(by.css("button[data-date='2019-08-11']"));
        browser.actions().mouseMove(grapBar).perform();
        const tooltip = grapBar.element(by.css('.bar')).element(by.css('.price-info')).element(by.css('.price-price'));
        // Wait for the tooltip to be visible
        browser.wait(EC.visibilityOf(tooltip),5000);
        return tooltip;
    };
    this.getNewDate = async function () {
        const selectedBar = element(by.css('.Button-No-Standard-Style.js-bar.item.selected'));
        // Wait for the selected bar to be visible
        browser.wait(EC.elementToBeClickable(selectedBar), 8000);
        const pre_selectedDate = await browser.wait(function () {
            // Getting the pre-selected date
            return selectedBar.getAttribute('data-date')
        });
        // Adding two days in the current selected date
        return moment(pre_selectedDate).add(2, 'days').format('YYYY-MM-DD');
    };
    this.getNewSelectedGraphBar = async function (barDate) {
        const newGraphBar = element(by.css("button[data-date='" + barDate + "']"));
        browser.wait(EC.elementToBeClickable(newGraphBar), 5000);
        await newGraphBar.click();
        return newGraphBar;
    };
    this.getSelectedBarStatus = function (newSelectGraphBar) {
        browser.wait(EC.visibilityOf(newSelectGraphBar),8000);
        browser.wait(async function () {
            const SelectedGraphBarAttributes = await newSelectGraphBar.getAttribute('class');
                if(SelectedGraphBarAttributes.includes('selected')){
                    return true
                }
        },5000);
        return newSelectGraphBar.getAttribute('class')
    };
    this.getSelectedBarPrice = async function () {
        const selectedPrice = element(by.css('.highlight-price'));
        browser.wait(EC.visibilityOf(selectedPrice),5000);
        return await selectedPrice.isPresent();
    };
    this.getSelectedPriceTextShown = async function () {
        const selectedPriceText = element(by.css('.hightlight'));
        browser.wait(EC.visibilityOf(selectedPriceText), 5000);
        return await selectedPriceText.isPresent();
    };
    this.getSearchBtnShown = async function () {
        const searchBtn = element(by.xpath("//a[contains(@aria-describedby,'-search-dates-description')]"));
        browser.wait(EC.visibilityOf(searchBtn), 5000);
        return await searchBtn.isPresent();
    };
    this.searchTheseDays = function () {
        const searchTheseDaysButton = element(by.xpath("//a[contains(@aria-describedby,'-search-dates-description')]"));
        searchTheseDaysButton.click();
        browser.wait(EC.invisibilityOf(searchTheseDaysButton),5000);
    };
    this.showDetails = function () {
        // Wait for the Graph to be populated so new data could be loaded
        const graphElement = element.all(by.css('.graph-col'));
        browser.wait(EC.visibilityOf(graphElement.get(1)),5000);
        const showDetailsBtn = element(by.xpath("//a[contains(@id,'-extra-info-details-link-toggleMore')]"));
        // Wait for the show details Btn to be clickable
        browser.wait(EC.elementToBeClickable(showDetailsBtn),5000);
        showDetailsBtn.click();
    };
    this.getDepartureDateInDetailsPanel = function () {
        let detailsPanel = element.all(by.xpath("//section[contains(@id,'-details-leg-details')]"));
        detailsPanel = detailsPanel.first();
        // Wait for the deatils drop down to be visible
        browser.wait(EC.visibilityOf(detailsPanel),5000);
        const detailsPanelDepartureDate = element.all(by.css('.leg-dates-set')).first();
        browser.wait(EC.visibilityOf(detailsPanelDepartureDate),5000);
        browser.wait(EC.visibilityOf(detailsPanelDepartureDate.element(by.css('div'))),5000);
        return detailsPanelDepartureDate.element(by.css('div'));
    };
    this.isSelectedPriceTextShownExist = async function () {
        const selectedPriceText = element(by.css('.hightlight'));
        return await selectedPriceText.isPresent();
    };
    this.isSearchTheseDaysButtonExist = async function () {
        const selectedPriceText = element(by.xpath("//a[contains(@aria-describedby,'-search-dates-description')]"));
        return await selectedPriceText.isPresent();
    };

};
module.exports = new homePage();