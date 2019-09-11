import {browser, by, element, ElementFinder} from "protractor";
import CommonHelper from "../helper/CommonHelper";
import moment from 'moment';
import TripPopup from "./TripPopup";

export default class AddTripPopup extends TripPopup {
    addTripPopup: ElementFinder = element(by.css("div[aria-label='Add a Trip']"));
    saveTripBtn: ElementFinder = this.addTripPopup.element(by.css("button[type='submit']"));

    async setTripDestination(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeClickable(this.destinationInputBox);
        await this.destinationInputBox.sendKeys(this.commonHelperObj.tripDestination);
        await this.commonHelperObj.waitForElementToBeClickable(this.destinationDropdownFirstElement);
        await this.destinationDropdownFirstElement.click();
    }
    async setTripName(): Promise<void> {
        await this.tripNameInputBox.clear();
        await this.tripNameInputBox.sendKeys(this.commonHelperObj.tripName);
    }
    async setTripDuration(): Promise<void> {
        let tripStartDate = moment(new Date()).add(30,'days');
        await this.selectStartDateFromCalender(tripStartDate);
        let tripEndDate = moment(tripStartDate).add(10,'days');
        await this.selectEndDateFromCalender(tripStartDate,tripEndDate);
    }
    async saveTrip(): Promise<void> {
        await this.saveTripBtn.click();
        await this.commonHelperObj.waitForElementToBeInvisible(this.addTripPopup);
    }
    private async selectStartDateFromCalender(tripStartDate: moment.Moment) {
        await this.startDateInputBox.click();
        const currentDay = new Date().getDate();
        const tripStartDay = tripStartDate.get("date");
        if(tripStartDay <= currentDay) {                                                                              // Means we have to go to next month
            await this.commonHelperObj.waitForElementToBeClickable(this.gotoNextMonthCalendarBtn);
            await this.gotoNextMonthCalendarBtn.click();
        }
        const startDateBtn = this.calendarDropdown.element(by.cssContainingText("div[role='button']",tripStartDay.toString()));
        await startDateBtn.click();
        await this.commonHelperObj.waitForElementToBeInvisible(this.gotoNextMonthCalendarBtn);
    }
    private async selectEndDateFromCalender(tripStartDate: moment.Moment, tripEndDate: moment.Moment) {
        await this.endDateInputBox.click();
        const tripStartDay = tripStartDate.get("date");
        const tripEndDay = tripEndDate.get("date");
        if(tripEndDay <= tripStartDay) {
            await this.commonHelperObj.waitForElementToBeClickable(this.gotoNextMonthCalendarBtn);
            await this.gotoNextMonthCalendarBtn.click();
        }
        const endDateBtn = this.calendarDropdown.element(by.cssContainingText("div[role='button']",tripEndDay.toString()));
        await endDateBtn.click();
        await this.commonHelperObj.waitForElementToBeInvisible(this.gotoNextMonthCalendarBtn);
    }
}