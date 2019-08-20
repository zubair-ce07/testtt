import {element, by, ElementFinder, ElementArrayFinder, browser} from 'protractor';
export default class HomePageElements {
    flightOrigin: ElementFinder = element(by.name('origin'));
    flightDestination: ElementFinder = element(by.name('destination'));
    flightDepartureDate: ElementFinder = element(by.css("div[id*='-dateRangeInput-display-start-inner']"));
    flightReturnDate: ElementFinder = element(by.css("div[id*='-dateRangeInput-display-end-inner']"));
    flightTravelers: ElementFinder = element(by.css("a[id*='-travelers-dialog']")).element(by.css('.label'));
    mainGraph: ElementFinder = element(by.css('.graph-grid'));
    searchBtn: ElementFinder = element(by.css("button[aria-label='Edit search']"));
    allVisibleGraphs: ElementArrayFinder = element.all(by.css('.graph-col'));
    newCalendarDate: ElementFinder = element(by.css("div[aria-label='September 10']"));
    graphBar: ElementFinder = element(by.css("button[data-date='2019-08-29']"));
    selectedGraphBar: ElementFinder = element(by.css('.Button-No-Standard-Style.js-bar.item.selected'));
    graphBarTooltip: ElementFinder = this.graphBar.element(by.css('.bar')).element(by.css('.price-info')).element(by.css('.price-price'));
    selectedGraphBarPrice: ElementFinder = element(by.css('.highlight-price'));
    selectedPriceLabel: ElementFinder = element(by.css('.hightlight'));
    searchTheseDaysBtn: ElementFinder = element(by.css("a[aria-describedby*='-search-dates-description']"));
    showDetailsBtn: ElementFinder = element(by.css("a[id*='-extra-info-details-link-toggleMore']"));
    allDetailsPanel: ElementArrayFinder = element.all(by.css("div[class='resultInner']"));
    allDetailsPanelDates: ElementArrayFinder = element.all(by.css('.leg-dates-set'));

    async getFlightOrigin(): Promise<any> {
        return await this.flightOrigin.getAttribute('value');
    }
    async getFlightDestination(): Promise<any> {
        return await this.flightDestination.getAttribute('value');
    }
    async getFlightDepartureDate(): Promise<any> {
        return await this.flightDepartureDate.getText();
    }
    async getFlightReturnDate(): Promise<any> {
        return await this.flightReturnDate.getText();
    }
    async getFlightTravelers(): Promise<any> {
        return await this.flightTravelers.getText();
    }
    async getGraph(): Promise<any> {
        return await this.mainGraph;
    }
    async clickSearchBtn(): Promise<void> {
        await this.searchBtn.click();
    }
    getAllVisibleGraphs(): any {
       return this.allVisibleGraphs;
    }
    async clickFlightReturnDate(): Promise<void> {
        await this.flightReturnDate.click();
    }
    getNewCalendarDate(): any {
        return this.newCalendarDate;
    }
    async clickNewCalendarDate(): Promise<any> {
       await this.getNewCalendarDate().click();
    }
    async hoverOverGraphBar(): Promise<any> {
        await browser.actions().mouseMove(this.graphBar).perform();
    }
    getGraphBarTooltip(): any {
        return this.graphBarTooltip;
    }
    getSelectedGraphBar(): any {
        return this.selectedGraphBar;
    }
    async getSelectedGraphBarDate(): Promise<any> {
        return await this.selectedGraphBar.getAttribute('data-date');
    }
    getNewGraphBar(barDate: string): any {
        return element(by.css("button[data-date='" + barDate + "']"))
    }
    getSelectedBarPrice(): any {
        return this.selectedGraphBarPrice;
    }
    getSelectedPriceLabel(): any {
        return this.selectedPriceLabel;
    }
    getSearchTheseDaysBtn(): any {
        return this.searchTheseDaysBtn;
    }
    async clickSearchTheseDaysBtn(): Promise<any> {
        await this.searchTheseDaysBtn.click();
    }
    getShowDetailsBtn(): any {
        return this.showDetailsBtn;
    }
    async clickShowDetailsBtn(): Promise<any> {
        await this.showDetailsBtn.click();
    }
    getDetailsPanel(): any {
        return this.allDetailsPanel;
    }
    async getDetailsPanelDepartureDate(): Promise<any> {
        return await this.allDetailsPanelDates.first()
    }
}