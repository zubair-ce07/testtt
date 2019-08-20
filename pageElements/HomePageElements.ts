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

    getFlightOrigin(): any {
        return this.flightOrigin.getAttribute('value');
    }
    getFlightDestination(): any {
        return this.flightDestination.getAttribute('value');
    }
    getFlightDepartureDate(): any {
        return this.flightDepartureDate.getText();
    }
    getFlightReturnDate(): any {
        return this.flightReturnDate.getText();
    }
    getFlightTravelers(): any {
        return this.flightTravelers.getText();
    }
    getGraph(): any {
        return this.mainGraph;
    }
    clickSearchBtn(): void {
        this.searchBtn.click();
    }
    getAllVisibleGraphs(): any {
       return this.allVisibleGraphs;
    }
    clickFlightReturnDate(): void {
        this.flightReturnDate.click();
    }
    getNewCalendarDate(): any {
        return this.newCalendarDate;
    }
    clickNewCalendarDate(): any {
        this.getNewCalendarDate().click();
    }
    hoverOverGraphBar(): any {
        browser.actions().mouseMove(this.graphBar).perform();
    }
    getGraphBarTooltip(): any {
        return this.graphBarTooltip;
    }
    getSelectedGraphBar(): any {
        return this.selectedGraphBar;
    }
    getSelectedGraphBarDate(): any {
        return this.selectedGraphBar.getAttribute('data-date');
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
    clickSearchTheseDaysBtn(): any {
        this.searchTheseDaysBtn.click();
    }
    getShowDetailsBtn(): any {
        return this.showDetailsBtn;
    }
    clickShowDetailsBtn(): any {
        this.showDetailsBtn.click();
    }
    getDetailsPanel(): any {
        return this.allDetailsPanel;
    }
    getDetailsPanelDepartureDate(): any {
        return this.allDetailsPanelDates.first()
    }
}