import { browser, by, element, ElementFinder, protractor } from "protractor";
import IFlight from "../interfaces/IFlight";
import { waitForElementVisibility, getTimeoutErrorMessage, convertMonthNameToShortName } from "../utils/common";
import IFlightSearchPage from "../interfaces/IFlightSearchPage";

class SiteMomontoPageObject implements IFlight, IFlightSearchPage {
    readonly flightsPageURL: string = "https://global.momondo.com/";
    readonly multiCityLegsSelector: string = ".multiCityLeg";
    private legNo: number;
    readonly firstOriginFieldName: string = "origin0";
    private currentFlightNumber: number;

    setLegNo(legNo: number): void {
        this.legNo = legNo;
    }

    getLegNo(): number {
        return this.legNo;
    }

    getMultiCityFlightSearchBox(): ElementFinder {
        return element(by.css(".searchform.multicity.mixedcabins"));
    }

    async selectFlightTypeMultiCity(): Promise<void> {
        const multiCityButton = element(by.css("[id$=-displayCat-set]")).element(by.css("[id$=-multicity-label]"));
        await multiCityButton.click();
    }

    async getOriginField(): Promise<ElementFinder> {
        const legNo = this.getLegNo();
        const originDisplayField = element(by.css(".searchform.multicity.mixedcabins")).element(by.name(`origin${legNo}`));
        await originDisplayField.click();
        return originDisplayField;
    }

    async getDestinationField(): Promise<ElementFinder> {
        const legNo = this.getLegNo();
        const originDisplayField = element(by.css(".searchform.multicity.mixedcabins")).element(by.name(`destination${legNo}`));
        await originDisplayField.click();
        return originDisplayField;
    }

    async selectFirstOptionFromOriginsDropdown(): Promise<void> {
        const originDropdownSelector = `[id$=-origin${this.getLegNo()}-smartbox-dropdown]`;
        await this.selectFirstOptionFromSmartDropDown(originDropdownSelector);
    }

    async selectFirstOptionFromDestinationDropdown(): Promise<void> {
        const destinationDropdownSelector = `[id$=-destination${this.getLegNo()}-smartbox-dropdown]`;
        await this.selectFirstOptionFromSmartDropDown(destinationDropdownSelector);
    }

    async selectFirstOptionFromSmartDropDown(dropdownSelector): Promise<void> {
        const dropdownElement = element(by.css(dropdownSelector));
        waitForElementVisibility(dropdownElement, 10000, "Timeout Error! origins dropdown is taking too long to appear in DOM");
        const origin = element.all(by.css(dropdownSelector)).first().all(by.css(".ap")).first();
        browser.actions().mouseMove(origin).perform();
        await origin.click();
    }

    async setFlightDepartureDate(): Promise<string> {
        const datePickerSelector = `[id$=-departDate${this.getLegNo()}]`;
        const datePicker = this.getMultiCityFlightSearchBox().element(by.css(datePickerSelector));
        await datePicker.click();

        const calendar = element(by.css(".Common-Widgets-Datepicker-Calendar"));
        waitForElementVisibility(calendar, 10000, getTimeoutErrorMessage("Departure Calendar"));

        const lastCalendarDate = element.all(by.css(".col-day")).last();
        await browser.actions().mouseMove(lastCalendarDate).perform();
        await lastCalendarDate.click();

        const selectedDate = calendar.element(by.css(".col-day.selected"));
        return await selectedDate.getAttribute("aria-label");
    }

    async setFlightTypeToBusiness(): Promise<void> {
        const flightTypeDropdownSelectorName = `[id$=-cabin_type${this.getLegNo()}-select]`;
        const flightTypeDropdown = element(by.css(".searchform.multicity.mixedcabins")).element(by.css(flightTypeDropdownSelectorName));
        await flightTypeDropdown.click();
        const selectedFlightOption = flightTypeDropdown.element(by.css("[title='Business']"));
        browser.actions().mouseMove(selectedFlightOption).perform();
        await selectedFlightOption.click();
    }

    async getSelectedTravelerText() {
        const travelerField = element.all(by.css('.searchform.multicity')).first().all(by.css(".travelersBlock.label"));
        const selectedTravelerFieldText = await travelerField.getText();
        return selectedTravelerFieldText;
    }

    async clickSearchButton(): Promise<void> {
        const searchButton = this.getMultiCityFlightSearchBox().element(by.css("[id$=-submit-multi]"));
        await searchButton.click();
        await this.waitForFlightSearchResultToComplete();
    }

    async waitForFlightSearchResultToComplete(): Promise<void> {
        const searchProgressBarSelector = ".Common-Results-SpinnerWithProgressBar.finished";
        const searchProgressBar = element(by.css(searchProgressBarSelector));

        let EC = protractor.ExpectedConditions;
        await browser.wait(EC.visibilityOf(searchProgressBar), 20000, getTimeoutErrorMessage("Flights search progress bar"));
        await browser.wait(EC.visibilityOf(element(by.cssContainingText(searchProgressBarSelector, "Search complete"))), 20000, "Timeout Error! Flights Search complete text 'Search complete' is taking too long to appear in DOM");
    }

    async isFlightsSearchPageDisplayed(): Promise<boolean> {
        const currentPageURL = await browser.getCurrentUrl();
        return currentPageURL.indexOf("/flight-search") !== -1;
    }

    getAppliedTravelerFilterField(): ElementFinder {
        return element(by.css("[id$=-multiCityTravelers]"));
    }

    async clickChangeSearchButton(): Promise<void> {
        const searchButton = element(by.css(".inline-search-container ")).element(by.css("[id$=-submit]"));
        await searchButton.click();
    }

    async getMultiCityFormOriginAndDestination(): Promise<{ flightOrigin: string, flightDestination: string }> {
        const originField = element(by.css(".searchform.multicity")).element(by.name(`origin${this.getLegNo()}`));
        const flightOrigin = await originField.getAttribute("value");

        const destinationField = element(by.css(".searchform.multicity")).element(by.name(`destination${this.getLegNo()}`));
        const flightDestination = await destinationField.getAttribute("value");
        return { flightOrigin, flightDestination };
    }

    async getMultiCityFormCabinClass(): Promise<string> {
        const cabinField = element(by.css(".searchform.multicity")).element(by.css(`[id$=-cabin_type${this.getLegNo()}-status]`));
        return await cabinField.getText();
    }

    async getMultiCityFormTraveler(): Promise<string> {
        const travelerField = element.all(by.css('.travelersBlock')).first().all(by.css(".label")).first();
        const selectedTravelerFieldText = await travelerField.getText();
        return selectedTravelerFieldText;
    }

    async getMultiCityFormDate(): Promise<string> {
        const dateField = element(by.css(`[id$=-depart_date${this.getLegNo()}-input]`));
        return await dateField.getText();
    }

    async getSearchedFlightsCount(): Promise<number> {
        this.waitForFlightSearchResultToComplete();
        const allFlights = element.all(by.css(".Flights-Results-FlightResultItem"));
        return await allFlights.count();
    }

    async getSearchedFlightTakeOffTime(flightResultNo: number): Promise<string> {
        this.waitForFlightSearchResultToComplete();
        const allFlights = element.all(by.css(".Flights-Results-FlightResultItem"));
        const flightItem = allFlights.get(flightResultNo);

        const secondFlightTakeOffDetail = flightItem.all(by.css("[id$=info-flights] li")).get(1).element(by.css(".top"));
        const takeOffTime = await secondFlightTakeOffDetail.getText();
        return takeOffTime.trim();
    }
}

export default SiteMomontoPageObject;