import {by, element, ElementFinder} from "protractor";
import moment from "moment";
import TripPopup from "./TripPopup";

export default class EditTripPopup extends TripPopup {

    editTripPopup: ElementFinder = element(by.css("div[aria-label='Edit Trip']"));
    saveTripBtn: ElementFinder = this.editTripPopup.element(by.css("button[type='submit']"));

    async editTripDestination(): Promise<void> {
        await this.commonHelperObj.waitForElementToBeClickable(this.destinationInputBox);
        await this.destinationInputBox.clear();
        await this.destinationInputBox.sendKeys(this.commonHelperObj.tripDestinationEdit)
        await this.commonHelperObj.waitForElementToBeClickable(this.destinationDropdownFirstElement);
        await this.destinationDropdownFirstElement.click();
    }
    async editTripName(): Promise<void> {
        await this.tripNameInputBox.clear();
        await this.tripNameInputBox.sendKeys(this.commonHelperObj.tripNameEdit);
    }
    async editTripDuration(): Promise<void> {
        let tripStartDate: any = await this.startDateInputBox.getAttribute('value');
        let tripEndDate: any = await this.endDateInputBox.getAttribute('value');
        await this.startDateInputBox.click();
        tripStartDate = await this.changeDateFormat(tripStartDate);
        const newTripStartDate = moment(tripStartDate).add(5,'days');
        await this.selectDateFromCalender(tripStartDate,newTripStartDate);
        await this.endDateInputBox.click();
        tripEndDate = await this.changeDateFormat(tripEndDate);
        const newTripEndDate = moment(tripEndDate).add(5,'days');
        await this.selectDateFromCalender(tripEndDate,newTripEndDate);
    }

    async getTripDetails(): Promise<object> {
        return {
            tripName: await this.tripNameInputBox.getAttribute('value'),
            tripStartDate: await this.startDateInputBox.getAttribute('value'),
            tripEndDate: await this.endDateInputBox.getAttribute('value'),
        }
    }
    async saveTrip(): Promise<void> {
        await this.saveTripBtn.click();
        await this.commonHelperObj.waitForElementToBeInvisible(this.editTripPopup);
    }
    async changeDateFormat(selectedDate: string) {
        await this.commonHelperObj.waitForElementToBeVisible(this.calendarDropdownHeading);
        let calendarHeading: any = await this.calendarDropdownHeading.getText();
        calendarHeading = calendarHeading.split(' ');
        let dateDataArray = selectedDate.split(' ');
        if(dateDataArray[2].length < 2) dateDataArray[2] = '0'+dateDataArray[2];
        return moment(calendarHeading[1]+'-'+moment().month(dateDataArray[1]).format("MM")+'-'+dateDataArray[2]);
    }
    private async selectDateFromCalender(oldDate: moment.Moment, newDate: moment.Moment) {
        const oldDay = oldDate.get("date");
        const newDay = newDate.get("date");
        if(newDay <= oldDay) {
            await this.commonHelperObj.waitForElementToBeClickable(this.gotoNextMonthCalendarBtn);
            await this.gotoNextMonthCalendarBtn.click();
        }
        const dateBtn = this.calendarDropdown.element(by.cssContainingText("div[role='button']",newDay.toString()));
        await dateBtn.click();
        await this.commonHelperObj.waitForElementToBeInvisible(this.gotoNextMonthCalendarBtn);
    }
}