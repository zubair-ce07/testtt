import {by, element, ElementFinder} from "protractor";
import CommonHelper from "../helper/CommonHelper";

export default class TripPopup {
    commonHelperObj = new CommonHelper();
    destinationInputBox: ElementFinder = element(by.css("input[placeholder='Destination*']"));
    destinationDropdownFirstElement: ElementFinder = element.all(by.css('#autocompleteResultItem_undefined')).first();
    tripNameInputBox: ElementFinder = element(by.css("input[placeholder='Trip name*']"));
    startDateInputBox: ElementFinder = element(by.css("input[placeholder='Start date*']"));
    endDateInputBox: ElementFinder = element(by.css("input[placeholder='End date*']"));
    gotoNextMonthCalendarBtn: ElementFinder = element(by.css("button[aria-label='Go to next month']"));
    calendarDropdown: ElementFinder = element(by.css('#react-root-popover'));
    calendarDropdownHeading: ElementFinder = this.calendarDropdown.element(by.css('h4'));
}