import moment from 'moment';
const homePage = function () {
    browser.ignoreSynchronization = true;
    const EC = protractor.ExpectedConditions;
    this.loadHomePage = async function() {
        await browser.get('https://global.momondo.com/flight-search/LON-NYC/2019-08-24/2019-09-22?sort=price_a');
    };
    this.getOrigin = function () {
        return element(by.name('origin')).getAttribute('value');
    };
    this.getDestination = function () {
        return element(by.name('destination')).getAttribute('value');
    };
    this.getDepartureDate = function () {
        return element(by.css("div[id*='-dateRangeInput-display-start-inner']")).getText();
    };
    this.getReturnDate = function () {
        return element(by.css("div[id*='-dateRangeInput-display-end-inner']")).getText();
    };
    this.getTravelers = function () {
        return element(by.css("a[id*='-travelers-dialog']")).element(by.css('.label')).getText();
    };
    this.isGraphVisible = function () {
        let graphElement = element(by.css('.graph-grid'));
        browser.wait(EC.visibilityOf(graphElement),5000);
        return graphElement.isDisplayed();
    };
    this.selectTripType = function (tripType) {
        element(by.css("label[title='"+tripType+"']")).click();
    };
    this.getMainVisibleGraphCount = function (operationType) {
        element(by.css("button[aria-label='Edit search']")).click();
        let graphElement = element.all(by.css('.graph-col'));
        if(operationType === 'first_half') {
            browser.wait(EC.invisibilityOf(graphElement.get(1)),5000);
        } else {
            browser.wait(EC.visibilityOf(graphElement.get(1)),5000);
        }
        graphElement = element.all(by.css('.graph-col'));
        return graphElement.count();
    };
    this.selectDateFromCalendar = function () {
        element(by.css("div[id*='-dateRangeInput-display-end-inner']")).click();
        const newCalendarDateElement = element(by.css("div[aria-label='September 10']"));
        browser.wait(EC.elementToBeClickable(newCalendarDateElement), 5000);
        newCalendarDateElement.click();
        browser.wait(EC.invisibilityOf(newCalendarDateElement), 5000);
    };
    this.getGraphBarTooltip = function () {
        const graphBar = element(by.css("button[data-date='2019-08-29']"));
        browser.actions().mouseMove(graphBar).perform();
        const tooltip = graphBar.element(by.css('.bar')).element(by.css('.price-info')).element(by.css('.price-price'));
        browser.wait(EC.visibilityOf(tooltip),5000);
        return tooltip.getText();
    };
    this.getNewDate = async function () {
        const selectedBar = element(by.css('.Button-No-Standard-Style.js-bar.item.selected'));
        browser.wait(EC.elementToBeClickable(selectedBar), 8000);
        const pre_selectedDate = selectedBar.getAttribute('data-date');
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
        return await selectedPrice.isDisplayed();
    };
    this.getSelectedPriceTextShown = async function () {
        const selectedPriceText = element(by.css('.hightlight'));
        browser.wait(EC.visibilityOf(selectedPriceText), 5000);
        return await selectedPriceText.isDisplayed();
    };
    this.isSearchBtnShown = async function () {
        const searchBtn = element(by.css("a[aria-describedby*='-search-dates-description']"));
        browser.wait(EC.visibilityOf(searchBtn), 5000);
        return await searchBtn.isDisplayed();
    };
    this.searchTheseDays = function () {
        const searchTheseDaysButton = element(by.css("a[aria-describedby*='-search-dates-description']"));
        searchTheseDaysButton.click();
        browser.wait(EC.invisibilityOf(searchTheseDaysButton),5000);
    };
    this.showDetails = function () {
        const graphElement = element.all(by.css('.graph-col'));
        browser.wait(EC.visibilityOf(graphElement.get(1)),5000);
        const showDetailsBtn = element(by.css("a[id*='-extra-info-details-link-toggleMore']"));
        browser.wait(EC.elementToBeClickable(showDetailsBtn),5000);
        showDetailsBtn.click();
    };
    this.getDepartureDateFromDetailsPanel = function () {
        let detailsPanel = element.all(by.css("div[class='resultInner']"));
        detailsPanel = detailsPanel.first();
        browser.wait(EC.visibilityOf(detailsPanel),5000);
        const detailsPanelDepartureDate = element.all(by.css('.leg-dates-set')).first();
        browser.wait(EC.visibilityOf(detailsPanelDepartureDate),5000);
        browser.wait(EC.visibilityOf(detailsPanelDepartureDate.element(by.css('div'))),5000);
        return detailsPanelDepartureDate.element(by.css('div')).getText();
    };
    this.isPricesShownTextExist = function () {
        return element(by.css('.hightlight'));
    };
    this.isSearchTheseDaysButtonExist = function () {
        return element(by.css("a[aria-describedby*='-search-dates-description']"));
    };

};
module.exports = new homePage();