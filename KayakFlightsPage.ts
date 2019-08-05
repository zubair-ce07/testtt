import {browser, $, element, by, protractor, promise, ElementFinder, ElementArrayFinder, ProtractorExpectedConditions, ExpectedConditions, Key} from 'protractor';
import { Helper } from './Helper';

export class KayakFlightsPage {

    kayakHelper = new Helper();
    kayakUrl: string = "https://www.kayak.com/flights";
    searchOptionsDropDown: ElementFinder = element(by.css("div[id$=switch-display]"));
    multipleCitiesOption: ElementFinder = element(by.css("li[id$=switch-option-3]"));
    selectedSearchOption: ElementFinder = element(by.css("div[id$=switch-display-status]"));
    multipleCitiesForm: ElementFinder = element(by.css("form[name=mc-searchform]"));
    legOneOfmultipleCitiesForm: ElementFinder = element(by.css("div[id$=multiCityLeg0]"));
    legTwoOfmultipleCitiesForm: ElementFinder = element(by.css("div[id$=multiCityLeg1]"));
    legThreeOfmultipleCitiesForm: ElementFinder = element(by.css("div[id$=multiCityLeg2]"));
    originAirportOfLegOne: ElementFinder = element(by.css("div[id$=origin0-airport-display]"));
    originAirportInputBoxOfLegOne: ElementFinder = element(by.css("input[id$=origin0-airport]"));
    originAirportOfLegTwo: ElementFinder = element(by.css("div[id$=origin1-airport-display]"));
    originAirportInputBoxOfLegTwo: ElementFinder = element(by.css("input[id$=origin1-airport]"));
    destinationAirportOfLegOne: ElementFinder = element(by.css("div[id$=destination0-airport-display]"));
    destinationAirportInputBoxOfLegOne: ElementFinder = element(by.css("input[id$=destination0-airport]"));
    destinationAirportOfLegTwo: ElementFinder = element(by.css("div[id$=destination1-airport-display]"));
    destinationAirportInputBoxOfLegTwo: ElementFinder = element(by.css("input[id$=destination1-airport]"));
    cabinsSelectBoxOfLegOne: ElementFinder = element(by.css("div[id$=cabin_type0-display]"));
    businessCabinOptionOfLegOne: ElementFinder = element(by.css("li[id$=cabin_type0-option-3]"));
    cabinsSelectBoxOfLegTwo: ElementFinder = element(by.css("div[id$=cabin_type1-display]"));
    businessCabinOfLegTwo: ElementFinder = element(by.css("li[id$=cabin_type1-option-3]"));
    dateBoxOfLegOne: ElementFinder = this.legOneOfmultipleCitiesForm.element(by.css("div[id$=display-start]"));
    dateBoxOfLegTwo: ElementFinder = this.legTwoOfmultipleCitiesForm.element(by.css("div[id$=display-start]"));
    dateToBeSelectedInLegOne: ElementFinder = element(by.css(`div[aria-label='${this.kayakHelper.getDate(6)}']`));
    dateToBeSelectedInLegTwo: ElementFinder = element(by.css(`div[aria-label='${this.kayakHelper.getDate(12)}']`));
    searchButton: ElementFinder = element(by.css("button[id$=submit-multi]"));

    async get(): Promise<void> {
        await browser.get(this.kayakUrl);
    }

    async setValue(element: ElementFinder, value: String): Promise<void> {
        for (let i: number = 0; i < value.length; i++) {
            await element.sendKeys(value.charAt(i));
        }
    }

    async clickSearchOptionsDropDown(): Promise<void> {
        await browser.wait(ExpectedConditions.visibilityOf(this.searchOptionsDropDown), 10000);
        await this.searchOptionsDropDown.click();
    }

    async selectMultipleCitiesOption(): Promise<void> {
        await this.clickSearchOptionsDropDown();
        await browser.wait(ExpectedConditions.visibilityOf(this.multipleCitiesOption), 10000);
        await this.multipleCitiesOption.click();
    }

    async multipleCitiesOptionSelected(): Promise<boolean> {
        let selectedSearchOption = await this.selectedSearchOption.getAttribute("data-value");
        return selectedSearchOption === "multicity";
    }

    async multipleCitiesFormDisplayed(): Promise<boolean> {
        return await this.multipleCitiesForm.isDisplayed();
    }

    async threeLegsDisplayedInMultipleCitiesForm(): Promise<boolean> {
        let legOnemultipleCitiesDisplayed = await this.legOneOfmultipleCitiesForm.isDisplayed();
        let legTwoOfmultipleCitiesDisplayed = await this.legOneOfmultipleCitiesForm.isDisplayed();
        let legThreeOfmultipleCitiesDisplayed = await this.legThreeOfmultipleCitiesForm.isDisplayed();
        return await (legOnemultipleCitiesDisplayed && legTwoOfmultipleCitiesDisplayed && legThreeOfmultipleCitiesDisplayed);
    }

    async pressEscape(element: ElementFinder): Promise<void> {
        await element.sendKeys(Key.ESCAPE);
    }

    async clearInputField(element: ElementFinder) {
        await element.clear();
    }

    async clickAirportInputField(elementToBeClicked: ElementFinder): Promise<void> {
        await browser.wait(ExpectedConditions.elementToBeClickable(elementToBeClicked), 10000);
        await elementToBeClicked.click();
    }

    async fillAirport(elementToBeClicked: ElementFinder, inputField: ElementFinder, value: String): Promise<void> {
        this.clickAirportInputField(elementToBeClicked);
        await this.clearInputField(inputField);
        await this.setValue(inputField, value);
        await this.pressEscape(inputField);  
    }

    async setValueOfOriginAirportInLegOne(origin: string): Promise<void> {
        await this.fillAirport(this.originAirportOfLegOne, this.originAirportInputBoxOfLegOne, origin);
    }

    async getValueOfOriginAirportInLegOne(): Promise<string> {
        return await this.originAirportOfLegOne.getText();
    }

    async setValueOfDestinationAirportInLegOne(destination: string): Promise<void> {
        await this.fillAirport(this.destinationAirportOfLegOne, this.destinationAirportInputBoxOfLegOne, destination);
    }

    async getValueOfDestinationAirportInLegOne(): Promise<string> {
        return await this.destinationAirportOfLegOne.getText();
    }

    async setValueOfOriginAirportInLegTwo(origin: string): Promise<void> {
        await this.fillAirport(this.originAirportOfLegTwo, this.originAirportInputBoxOfLegTwo, origin);
    }

    async getValueOfOriginAirportInLegTwo(): Promise<string> {
        return await this.originAirportOfLegTwo.getText();
    }

    async setValueOfDestinationAirportInLegTwo(destination: string): Promise<void> {
        await this.fillAirport(this.destinationAirportOfLegTwo, this.destinationAirportInputBoxOfLegTwo, destination);
    }

    async getValueOfDestinationAirportInLegTwo(): Promise<string> {
        return await this.destinationAirportOfLegTwo.getText();
    }

    async clickCabinsSelectBoxOfLegOne(): Promise<void> {
        await this.cabinsSelectBoxOfLegOne.click();
    }

    async selectBusinessCabinInLegOne(): Promise<void> {
        await this.businessCabinOptionOfLegOne.click();
    }

    async clickCabinsSelectBoxOfLegTwo(): Promise<void> {
        await browser.wait(ExpectedConditions.elementToBeClickable(this.cabinsSelectBoxOfLegTwo), 10000);
        await this.cabinsSelectBoxOfLegTwo.click();
    }

    async selectBusinessCabinInLegTwo(): Promise<void> {
        await this.businessCabinOfLegTwo.click();
    }

    async getSelectedCabinOfLegOne(): Promise<string> {
        return await this.cabinsSelectBoxOfLegOne.getText();
    }

    async getSelectedCabinOfLegTwo(): Promise<string> {
        return await this.cabinsSelectBoxOfLegTwo.getText();
    }

    async clickDateBoxOfLegOne(): Promise<void> {
        await browser.wait(ExpectedConditions.elementToBeClickable(this.dateBoxOfLegOne), 10000);
        await this.dateBoxOfLegOne.click();
    }

    async clickDateBoxOfLegTwo(): Promise<void> {
        await browser.wait(ExpectedConditions.elementToBeClickable(this.dateBoxOfLegTwo), 10000);
        await this.dateBoxOfLegTwo.click();
    }

    async selectDateOfLegOne(): Promise<void> {
        await browser.wait(ExpectedConditions.visibilityOf(this.dateToBeSelectedInLegOne), 10000);
        await this.dateToBeSelectedInLegOne.click();
    }

    async getSelectedDateOfLegOne(): Promise<boolean> {
        return await this.dateToBeSelectedInLegOne.getAttribute("aria-selected") === "true";
    }

    async selectDateOfLegTwo(): Promise<void> {
        await browser.wait(ExpectedConditions.visibilityOf(this.dateToBeSelectedInLegTwo), 10000);
        await this.dateToBeSelectedInLegTwo.click();
    }

    async getSelectedDateInLegTwo(): Promise<boolean> {
        return await this.dateToBeSelectedInLegTwo.getAttribute("aria-selected") === "true";
    }

    async clickSearchButton(): Promise<void> {
        await browser.wait(ExpectedConditions.elementToBeClickable(this.searchButton), 10000);
        await this.searchButton.click();
    }
}