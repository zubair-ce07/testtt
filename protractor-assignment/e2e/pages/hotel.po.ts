import { browser, by, element, ElementFinder , $ , $$, ElementArrayFinder } from 'protractor';

export class AppHotelPage {
async navigateTo () : Promise<string> {
return await browser.get(browser.baseUrl);
}
async navigateToHotel () : Promise<string> {
    return await browser.get(`${browser.baseUrl}/hotels`);
}
getHotelLink () : ElementFinder {
return element(by.css('.Common-Layout-StyleJamNavigation ul li.js-vertical-hotels'));
}
getOriginInputWrapper () : ElementFinder {
return element(by.css('[id$=location-display-inner]'));
}
getOriginInput () : ElementFinder {
 return element(by.css('[id$=location-textInputWrapper] > input'));
}
getOriginDropdown () : ElementFinder {
    return element(by.css('[id$=location-smartbox-dropdown] > ul > li:first-child'));
}
getStartDate () : ElementFinder {
return element(by.css('[id$=dateRangeInput-display-start]'));
}
getEndDate () : ElementFinder {
return element(by.css('[id$=dateRangeInput-display-end]'));
}
getDisplayText () : ElementFinder {
return element.all(by.css('[id$=roomsGuestsDropdown-trigger] div.js-label')).first();
}
getSearchButton () : ElementFinder {
return element(by.css('[id$=formGridSearchBtn]'));
}
}
