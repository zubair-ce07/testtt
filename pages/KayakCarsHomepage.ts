import {by, element} from "protractor";
import CommonHelper from "../helper/CommonHelper";

export default class KayakCarsHomepage {
    commonHelperObj = new CommonHelper();

    dropOffStatus = element(by.css("div[id*='-switch-display-status']"));
    dropOffLabel = element(by.css("div[id$='-switch-display']"));
    differentDropOffOption = element(by.css("li[aria-label='Different drop-off']"));
    departureDateInput = element(by.css("div[id$='-dateRangeInput-display-start']"));
    calendar = element(by.css("div[id$='-cal-animationWrapper']"));
    departureDateInputBox = element(by.css("div[id$='-pickup-date-input']"));
    arrivalDateInputBox = element(by.css("div[id$='-dropoff-date-input']"));
    originInput = element(by.css("div[id$='-pickup-display']"));
    originInputBox = element(by.css("input[id$='-pickup']"));
    originInputDropdown = element(by.css("div[id$='-pickup-smartbox-dropdown']"));
    originDropdownFirstOption = this.originInputDropdown.all(by.css('li')).first();
    destinationInput = element(by.css("div[id$='-dropoff-display']"));
    destinationInputBox = element(by.css("input[id$='-dropoff']"));
    destinationInputDropdown = element(by.css("div[id$='-dropoff-smartbox-dropdown']"));
    destinationDropdownFirstOption = this.destinationInputDropdown.all(by.css('li')).first();
    carsSearchBtn = element(by.css("button[aria-label='Search cars']"));


    async getDropOffStatus(): Promise<string> {
        await this.commonHelperObj.waitForElementToBeVisible(this.dropOffStatus);
        return await this.dropOffStatus.getText();
    }
    async clickDropOffLabel(): Promise<void> {
        await this.dropOffLabel.click();
    }
    async isDifferentDropOffOptionClickable(): Promise<any> {
        await this.commonHelperObj.waitForElementToBeClickable(this.differentDropOffOption);
        return await this.differentDropOffOption.isDisplayed();
    }
    async clickDifferentDropOffOption(): Promise<void> {
        await this.differentDropOffOption.click();
    }
    async isDestinationFieldVisible(): Promise<boolean> {
        return await this.destinationInput.isDisplayed();
    }
    async clickDepartureInput(): Promise<void> {
        await this.departureDateInput.click();
    }
    async getSelectedDepartureDate(): Promise<string> {
        await this.commonHelperObj.waitForElementToBeVisible(this.calendar);
        return await this.departureDateInputBox.getText();
    }
    async getSelectedArrivalDate(): Promise<string> {
        await this.arrivalDateInputBox.click();
        return await this.arrivalDateInputBox.getText()
    }
    async setOrigin(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeClickable(this.originInput);
        await this.originInput.click();
        await this.originInputBox.sendKeys('LHR');
        await this.clickOriginDropdownFirstOption();
    }
    async clickOriginDropdownFirstOption(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeVisible(this.originInputDropdown);
        await this.commonHelperObj.waitForElementToBeClickable(this.originDropdownFirstOption);
        await this.originDropdownFirstOption.click();
    }
    async isOriginAdded(): Promise<string> {
        await this.commonHelperObj.waitForElementToBeInvisible(this.originInputBox);
        return await this.originInputBox.getAttribute('aria-expanded');
    }
    async setDestination(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeVisible(this.destinationInput);
        await this.destinationInput.click();
        await this.destinationInputBox.sendKeys('LHR');
        await this.clickDestinationDropdownFirstOption();
    }
    async clickDestinationDropdownFirstOption():Promise<void> {
        await this.commonHelperObj.waitForElementToBeVisible(this.destinationInputDropdown);
        await this.commonHelperObj.waitForElementToBeClickable(this.destinationDropdownFirstOption);
        await this.destinationDropdownFirstOption.click();
    }
    async isDestinationAdded(): Promise<string> {
        await this.commonHelperObj.waitForElementToBeInvisible(this.destinationInputBox);
        return await this.destinationInputBox.getAttribute('aria-expanded');
    }
    async clickSearchBtn(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeClickable(this.carsSearchBtn);
        await this.carsSearchBtn.click();
    }
}