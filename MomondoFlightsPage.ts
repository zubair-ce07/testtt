import {browser, $, element, by, protractor, promise, ElementFinder, ElementArrayFinder, ProtractorExpectedConditions, ExpectedConditions, Key} from 'protractor';
import {Helper} from './Helper';

export class MomondoFlightsPage {

    helper = new Helper();
    momondoUrl: string = "https://global.momondo.com/flights";
    searchOptionsDropDown: ElementFinder = element(by.css("div[id$=switch-display]"));
    multipleCitiesOption: ElementFinder = element(by.css("label[id$=multicity-label]"));
    searchSelectedOption: ElementFinder = element(by.css("div[id$=switch-display-status]"));
    multipleCitiesForm: ElementFinder = element(by.css("form[name=mc-searchform]"));
    legOneOfmultipleCitiesForm: ElementFinder = element(by.css("div[id$=multiCityLeg0]"));
    legTwoOfmultipleCitiesForm: ElementFinder = element(by.css("div[id$=multiCityLeg1]"));
    legThreeOfmultipleCitiesForm: ElementFinder = element(by.css("div[id$=multiCityLeg2]"));
    originAirportInputBoxOfLegOne: ElementFinder = element(by.css("input[id$=origin0]"));
    originAirportInputBoxOfLegTwo: ElementFinder = element(by.css("input[id$=origin1]"));
    destinationAirportInputBoxOfLegOne: ElementFinder = element(by.css("input[id$=destination0]"));
    destinationAirportInputBoxOfLegTwo: ElementFinder = element(by.css("input[id$=destination1]"));
    cabinsSelectBoxOfLegOne: ElementFinder = element(by.css("select[id$=cabin_type0-select]"));
    businessCabinOptionOfLegOne: ElementFinder = this.cabinsSelectBoxOfLegOne.element(by.css("option[title=Business]"));
    cabinsSelectBoxOfLegTwo: ElementFinder = element(by.css("div[id$=cabin_type1]"));
    businessCabinOptionOfLegTwo: ElementFinder = this.cabinsSelectBoxOfLegTwo.element(by.css("option[title=Business]"));
    dateBoxOfLegOne: ElementFinder = this.legOneOfmultipleCitiesForm.element(by.css("div[id$=departDate0]"));
    dateBoxOfLegTwo: ElementFinder = this.legTwoOfmultipleCitiesForm.element(by.css("div[id$=departDate1]"));
    dateToBeSelectedInLegOne: ElementFinder = element(by.css(`div[aria-label='${this.helper.getDate(6)}']`));
    dateToBeSelectedInLegTwo: ElementFinder = element(by.css(`div[aria-label='${this.helper.getDate(12)}']`));
    searchButton: ElementFinder = element(by.css("button[id$=submit-multi]"));

    async get(): Promise<void> {
        await browser.get(this.momondoUrl);
    }

    async setValue(element: ElementFinder, value: String): Promise<void> {
        for (let i: number = 0; i < value.length; i++) {
            await browser.sleep(1000);
            await element.sendKeys(value.charAt(i));
        }
    }

    async selectMultipleCitiesOption(): Promise<void> {
        await this.multipleCitiesOption.click();
    }

    async multipleCitiesOptionSelected(): Promise<boolean> {
        let multipleCityFocus = await this.multipleCitiesOption.getAttribute("class");
        return await multipleCityFocus.indexOf("focus") !== -1;
    }

    async multipleCitiesFormDisplayed(): Promise<boolean> {
        return await this.multipleCitiesForm.isDisplayed();
    }

    async threeLegsDisplayedInMultipleCitiesForm(): Promise<boolean> {
        let legOneOfmultipleCitiesDisplayed = await this.legOneOfmultipleCitiesForm.isDisplayed();
        let legTwoOfmultipleCitiesDisplayed = await this.legTwoOfmultipleCitiesForm.isDisplayed();
        let legThreeOfmultipleCitiesLegDisplayed = await this.legThreeOfmultipleCitiesForm.isDisplayed();
        return await (legOneOfmultipleCitiesDisplayed && legTwoOfmultipleCitiesDisplayed && legThreeOfmultipleCitiesLegDisplayed);
    }

    async pressEnter(element: ElementFinder): Promise<void> {
        await element.sendKeys(Key.ENTER);
    }

    async pressEscape(element: ElementFinder): Promise<void> {
        await element.sendKeys(Key.ESCAPE);
    }

    async clearInputField(element: ElementFinder) {
        await element.clear();
    }

    async clickLegOneOriginAirport(): Promise<void> {
        await browser.wait(ExpectedConditions.elementToBeClickable(this.originAirportInputBoxOfLegOne), 10000);
        await this.originAirportInputBoxOfLegOne.click();
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
        await this.fillAirport(this.originAirportInputBoxOfLegOne, this.originAirportInputBoxOfLegOne, origin);
    }

    async getValueOfOriginAirportInLegOne(): Promise<string> {
        return await this.originAirportInputBoxOfLegOne.getText();
    }

    async setValueOfDestinationAirportInLegOne(destination: string): Promise<void> {
        await this.fillAirport(this.destinationAirportInputBoxOfLegOne, this.destinationAirportInputBoxOfLegOne, destination);
    }

    async getValueOfDestinationAirportInLegOne(): Promise<string> {
        return await this.destinationAirportInputBoxOfLegOne.getText();
    }

    async setValueOfOriginAirportInLegTwo(origin: string): Promise<void> {
        await this.fillAirport(this.originAirportInputBoxOfLegTwo, this.originAirportInputBoxOfLegTwo, origin);
    }

    async getValueOfOriginAirportInLegTwo(): Promise<string> {
        return await this.originAirportInputBoxOfLegTwo.getText();
    }

    async setValueOfDestinationAirportInLegTwo(destination: string): Promise<void> {
        await this.fillAirport(this.destinationAirportInputBoxOfLegTwo, this.destinationAirportInputBoxOfLegTwo, destination);
    }

    async getValueOfDestinationAirportInLegTwo(): Promise<string> {
        return await this.destinationAirportInputBoxOfLegTwo.getText();
    }

    async clickCabinsSelectBoxOfLegOne(): Promise<void> {
        await this.cabinsSelectBoxOfLegOne.click();
    }

    async selectBusinessCabinInLegOne(): Promise<void> {
        await browser.wait(ExpectedConditions.elementToBeClickable(this.businessCabinOptionOfLegOne), 10000);
        await this.businessCabinOptionOfLegOne.click();
        await this.pressEscape(this.businessCabinOptionOfLegOne);
    }

    async clickCabinsSelectBoxOfLegTwo(): Promise<void> {
        await browser.wait(ExpectedConditions.visibilityOf(this.cabinsSelectBoxOfLegTwo), 10000);
        await this.cabinsSelectBoxOfLegTwo.click();
    }

    async selectBusinessCabinInLegTwo(): Promise<void> {
        await browser.wait(ExpectedConditions.elementToBeClickable(this.businessCabinOptionOfLegTwo), 10000);
        await this.businessCabinOptionOfLegOne.click();
        await this.pressEscape(this.businessCabinOptionOfLegOne);
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
        await browser.wait(ExpectedConditions.visibilityOf(this.dateToBeSelectedInLegOne), 10000);
        await this.dateToBeSelectedInLegOne.click();
    }

    async getSelectedDateInLegTwo(): Promise<boolean> {
        return await this.dateToBeSelectedInLegTwo.getAttribute("aria-selected") === "true";
    }

    async clickSearchButton(): Promise<void> {
        await browser.wait(ExpectedConditions.elementToBeClickable(this.searchButton), 10000);
        await this.searchButton.click();
    }
}