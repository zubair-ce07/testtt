import {by, element, ElementFinder, browser} from "protractor";
import TripPopup from "./TripPopup";

export default class DeleteTripPopup extends TripPopup {
    deleteTripPopup: ElementFinder = element(by.css("div[aria-label='Delete this trip']"));
    tripThumbnail: ElementFinder = this.deleteTripPopup.element(by.css('img'));
    deleteTripBtn: ElementFinder = element(by.cssContainingText("button","Delete"));

    async deleteTrip(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeVisible(this.tripThumbnail);
        await this.commonHelperObj.waitForElementToBeClickable(this.deleteTripBtn);
        await this.deleteTripBtn.click();
        await this.commonHelperObj.waitForElementToBeInvisible(this.deleteTripPopup);
    }
}