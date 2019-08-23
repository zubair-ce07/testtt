import { browser, by, element, ElementFinder, protractor } from "protractor";
import IFlight from "../interfaces/IFlight";
import { waitForElementVisibility, getTimeoutErrorMessage } from "../utils/common";
import IFlightSearchPage from "../interfaces/IFlightSearchPage";

class SiteKayakPageObject implements IFlight, IFlightSearchPage {
    readonly flightsPageURL: string = "https://www.kayak.com/flights";
    readonly multiCityLegsSelector: string = ".js-multiCityLeg";
    private legNo: number;

    setLegNo(legNo: number): void {
        this.legNo = legNo;
    }

    getLegNo(): number {
        return this.legNo;
    }

    async selectFlightTypeMultiCity(): Promise<void> {
        const tripType = element(by.css(".Base-Search-SearchForm")).element(by.css("[id$=-switch-display-status]"));
        await tripType.click();
        const multiCity = element.all(by.css("[data-value=multicity]")).filter((element) => element.isDisplayed());
        await multiCity.click();
    }

    async getOriginField(): Promise<ElementFinder>  {
        const legNo = this.getLegNo();
        const originDisplayField = element(by.css(".js-searchForm")).element(by.css(`[id$=-origin${legNo}-airport-display]`));
        await originDisplayField.click();

        const inputFieldContainer = element.all(by.css(`[id$=-origin${legNo}-airport-smarty-window]`)).first();
        let EC = protractor.ExpectedConditions;
        browser.wait(EC.visibilityOf(inputFieldContainer), 10000, getTimeoutErrorMessage("Smart Dropdown"));
        return inputFieldContainer.element(by.name(`origin${this.getLegNo()}`));
    }

    async getDestinationField(): Promise<ElementFinder>  {
        const legNo = this.getLegNo();
        const destinationDisplayField = element(by.css(".js-searchForm")).element(by.css(`[id$=-destination${legNo}-airport-display]`));
        await destinationDisplayField.click();

        const inputFieldContainer = element.all(by.css(`[id$=-destination${legNo}-airport-smarty-window]`)).first();
        let EC = protractor.ExpectedConditions;
        browser.wait(EC.visibilityOf(inputFieldContainer), 10000, "Timeout Error! origin smartbox dropdown is taking too long to appear in DOM");
        return inputFieldContainer.element(by.name(`destination${this.getLegNo()}`));
    }

    async selectFirstOptionFromOriginsDropdown(): Promise<void> {
        const originDropdownSelector = `[id$=-origin${this.getLegNo()}-airport-smarty-content]`;
        await this.selectFirstOptionFromSmartDropDown(originDropdownSelector);
    }

    async selectFirstOptionFromDestinationDropdown(): Promise<void> {
        const dropdownSelector = `[id$=-destination${this.getLegNo()}-airport-smarty-content]`;
        await this.selectFirstOptionFromSmartDropDown(dropdownSelector);
    }

    async selectFirstOptionFromSmartDropDown(dropdownSelector): Promise<void> {
        waitForElementVisibility(element(by.css(dropdownSelector)), 10000, "Timeout Error! smartbox dropdown is taking too long to appear in DOM");
        const dropdowns = element.all(by.css(dropdownSelector)).filter(elem => elem.isDisplayed());
        const origin = dropdowns.first().all(by.css('li')).first();
        browser.actions().mouseMove(origin).perform();
        await origin.click();
    }

    async setFlightDepartureDate(): Promise<string> {
        const datePicker = element(by.css(`[id$=-js-multiCityLeg${this.getLegNo()}]`)).element(by.css(".Common-Widgets-Datepicker-DateModal"));
        await datePicker.click();

        const calendar = element(by.css(".Common-Widgets-Datepicker-DateModal-overlay-content.visible"));
        waitForElementVisibility(calendar, 10000, getTimeoutErrorMessage("Departure Calendar"));

        const lastCalendarDate = element.all(by.css(".col.day.selected")).last();
        await browser.actions().mouseMove(lastCalendarDate).perform();
        await lastCalendarDate.click();

        return await lastCalendarDate.getAttribute("aria-label");
    }

    async setFlightTypeToBusiness(): Promise<void> {
        const legNo = this.getLegNo();
        const flightTypeDisplayField = element(by.css(`[id$=-js-multiCityLeg${legNo}]`)).element(by.css(`[id$=-cabin_type${legNo}]`));
        await flightTypeDisplayField.click();

        const flightTypeDropdown = element(by.css(`[id$=-cabin_type${legNo}-content]`));
        waitForElementVisibility(flightTypeDropdown, 10000, getTimeoutErrorMessage("Flight Type"));
        const selectedFlightOption = flightTypeDropdown.element(by.css(`[id$=-cabin_type${legNo}-option-3]`));
        browser.actions().mouseMove(selectedFlightOption).perform();
        await selectedFlightOption.click();
    }

    async getSelectedTravelerText(): Promise<string> {
        const travelerField = element.all(by.css(".col-travelers")).filter(elem => elem.isDisplayed()).all(by.css(".col.js-label")).first();
        return await travelerField.getText();
    }

    async clickSearchButton(): Promise<void> {
        const searchButton = element(by.css(".MultiForm__SecondaryGrid")).element(by.css("[id$=-submit-multi]"));
        await searchButton.click();
        await this.waitForFlightSearchResultToComplete();
    }

    async waitForFlightSearchResultToComplete(): Promise<void> {
        const searchList = element(by.css("[id=searchResultsList]"));
        let EC = protractor.ExpectedConditions;
        await browser.wait(EC.visibilityOf(searchList), 20000, getTimeoutErrorMessage("Flights search result list"));
    }

    async isFlightsSearchPageDisplayed(): Promise<boolean> {
        const flightSearchSection = element(by.css(".FlightsSearch"));
        return await flightSearchSection.isDisplayed();
    }

    getAppliedTravelerFilterField(): ElementFinder {
        return element(by.css(".col-controls")).element(by.css(".js-label"));
    }

    async getMultiCityFormOriginAndDestination(): Promise<{flightOrigin: string, flightDestination:string}> {
        const originField = element(by.css(`[id$=-origin${this.getLegNo()}-airport-display-inner]`));
        const flightOrigin = await originField.getText();

        const destinationField = element(by.css(`[id$=-destination${this.getLegNo()}-airport-display-inner]`));
        const flightDestination = await destinationField.getText();
        return { flightOrigin, flightDestination };
    }

    async getMultiCityFormCabinClass(): Promise<string> {
        const cabinField = element(by.css("[id$=-cabin_type1-display-status]"));
        return await cabinField.getText();
    }

    async getMultiCityFormTraveler(): Promise<string> {
        const travelerField = element(by.css("[id$=-inlineSearch]")).element(by.css(".col.js-label"));
        return await travelerField.getText();
    }
}

export default SiteKayakPageObject;