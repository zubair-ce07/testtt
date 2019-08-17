import { Aliases } from './../shared/constants';
import { browser, by, element, ElementFinder , $ , $$, ElementArrayFinder } from 'protractor';
import { browserWaitHandler } from '../shared/utils';

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
getDestinationInputWrapper () : ElementFinder {
return element(by.css('[id$=location-display-inner]'));
}
getDestinationInput () : ElementFinder {
 return element(by.css('[id$=location-textInputWrapper] > input'));
}
getHotelOriginContainerWrapper () : ElementFinder {
return element(by.css('[id$=location-display]'));
}
getSearchResultsList () : ElementArrayFinder {
  return  element.all(by.css('[id$=searchResultsList] .normalResults div[tabindex]'));
 }
getDestinationDropdown () : ElementFinder {
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
async getSearchHotelHandler () : Promise<number>  {
    await this.getDestinationInputWrapper().click();
    await this.getDestinationInput().sendKeys(Aliases.originSearchKeywork);
    browserWaitHandler(this.getDestinationDropdown());
    await this.getDestinationDropdown().click();
    await this.getSearchButton().click();
    browserWaitHandler(this.getSearchResultsList().first());
    const hotelResultList : ElementArrayFinder = this.getSearchResultsList();
    const hotelResultCount : number = await hotelResultList.count();
    return hotelResultCount;
}
}
