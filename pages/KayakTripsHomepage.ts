import CommonHelper from "../helper/CommonHelper";
import {by, element, ElementFinder, ElementArrayFinder} from "protractor";

export default class KayakTripsHomepage {
    commonHelperObj = new CommonHelper();

    tripsPageMainContent: ElementFinder = element(by.css('.pageContent '));
    createManualTripBtn: ElementFinder = element(by.cssContainingText('button','Create a trip manually'));
    editTripBtn: ElementFinder = element(by.css("button[aria-label='Edit trip']"));
    moreTripOptionsBtn: ElementFinder = element(by.css("button[aria-label='More']"));
    deleteTripOptions: ElementFinder = element(by.cssContainingText("button[role='menuitem']",'Delete trip'));
    tripName: ElementFinder = this.tripsPageMainContent.element(by.css('h1'));
    tripDuration: ElementArrayFinder = this.tripsPageMainContent.all(by.css('div'));

    async isTripsPageLoaded(): Promise<boolean> {
        await this.commonHelperObj.waitForElementToBeVisible(this.tripsPageMainContent);
        return this.tripsPageMainContent.isDisplayed();
    }
    async clickCreateTripBtn(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeVisible(this.createManualTripBtn);
        await this.createManualTripBtn.click();
    }
    async isTripSaved(): Promise<boolean> {
        await this.commonHelperObj.waitForElementToBeClickable(this.editTripBtn);
        return await this.editTripBtn.isDisplayed();
    }
    async clickEditTripBtn(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeClickable(this.editTripBtn);
        await this.editTripBtn.click();
    }
    async clickMoreOptionsBtn(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeVisible(this.moreTripOptionsBtn);
        await this.moreTripOptionsBtn.click();
    }
    async clickDeleteTrip(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeVisible(this.deleteTripOptions);
        await this.deleteTripOptions.click();
    }
    async isTripDetailsSavedCorrectly() {
        await this.commonHelperObj.waitForElementToBeVisible(this.tripName);
        const savedTripName = await this.tripName.getText();
        const tripDuration = await this.tripDuration.get(4).getText();
        const tripDurationArray = tripDuration.split(' – ');
        const tripEndDateArray = tripDurationArray[1].split(' (');
        const tripSavedData = {
            tripName: savedTripName,
            tripStartDate: tripDurationArray[0],
            tripEndDate: tripEndDateArray[0]
        };
        return JSON.stringify(tripSavedData);
    }
}