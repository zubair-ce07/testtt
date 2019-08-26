import {by, element, ElementFinder} from "protractor";
import CommonElements from "./CommonElements";

export default class HotelsFrontPageElements {
    commonElementsObj = new CommonElements();
    hotelsOrigin: ElementFinder = element(by.css("div[id*='-fieldGridLocationCol']"));
    hotelsStartDate: ElementFinder = element(by.css("div[id*='-dateRangeInput-display-start-inner']"));
    hotelsEndDate: ElementFinder = element(by.css("div[id*='-dateRangeInput-display-end']"));
    hotelsGuestField : ElementFinder = element(by.css("button[id*='-roomsGuestsDropdown-trigger']"))
                                        .element(by.css('div')).element(by.css('div')).element(by.css('div')).element(by.css('div'));
    hotelsOriginInput: ElementFinder = element(by.css("input[aria-label='Destination input']"));
    originDropdown: ElementFinder = element(by.css("div[id*='-location-smartbox-dropdown']"));
    originFirstDropdownOption: ElementFinder = this.originDropdown.element(by.css('ul')).element(by.css('li'));
    searchHotelsBtn: ElementFinder = element(by.css("div[id*='-formGridButtonCol']"));

    getHotelsBtn (): ElementFinder {
        return this.commonElementsObj.hotelsFrontPageLink
    }
    getHotelsOriginField (): ElementFinder {
        return this.hotelsOrigin
    }
    getHotelsStartDateField (): ElementFinder {
        return this.hotelsStartDate
    }
    getHotelsEndDateField (): ElementFinder {
        return this.hotelsEndDate
    }
    getHotelsGuestField (): ElementFinder {
        return this.hotelsGuestField;
    }
    getHotelsOriginInputField(): ElementFinder {
        return this.hotelsOriginInput;
    }
    getOriginDropdown(): ElementFinder {
        return this.originDropdown;
    }
    getFirstResultOfOriginDropdown(): ElementFinder {
        return this.originFirstDropdownOption;
    }
    getSearchHotelsBtn(): ElementFinder {
        return this.searchHotelsBtn;
    }
}