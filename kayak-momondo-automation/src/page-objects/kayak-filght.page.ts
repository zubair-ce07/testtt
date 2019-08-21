import { IFlight } from './../core/interfaces/flight';
import { element, by, $, ElementFinder, Key } from 'protractor';
import { browserWaitHandler } from '../core/utils';
export class KayakFlightsPageObject implements IFlight {
    selectMultiCity = async () : Promise <void>  => {
     await  element.all(by.css('[id$=switch-display]')).first().click();
     await element.all(by.css('[id$=switch-list-wrapper] ul li:last-child')).first().click();
    }
    getMultiCitySection = () : ElementFinder => element(by.css('[id$=multi-fields]'));
    getFirstOriginCitySelector = () : ElementFinder => element(by.css('[id$=origin0-airport-display]'));
    getFirstOriginCityDropdown = () => element(by.css('[id$=origin0-airport-nearby] ul li:first-child'));
    getFirstDestinationCityDropdown = () => element(by.css('[id$=destination0-smartbox-dropdown] ul li:first-child'));
    getFirstDestinationCitySelector = () : ElementFinder => element(by.css('input[id$=destination0]'));
    getDepartureDateSelector = () : ElementFinder => element(by.css('[id$=departDate0-input]'));
    getDepartureTimeSelector = () : ElementFinder => element(by.css('[id$=depart_time0-select]'));
    selectFlightTypeSelector = () : ElementFinder => element(by.css('[id$=cabin_type0-select]'));
    getFirstOriginCitySelectorValue = async () => element(by.css('input[id$=origin0]')).getAttribute('value');
    getFirstDestinationCitySelectorValue = async () => element(by.css('input[id$=destination0]')).getAttribute('value');
    selectFirstOriginCity = async () : Promise<void> => {
        browserWaitHandler(this.getFirstOriginCitySelector());
        await this.getFirstOriginCitySelector().click();
        await element(by.css('input[id$=origin0-airport]')).clear();
        await element(by.css('input[id$=origin0-airport]')).sendKeys('FRA');
        browserWaitHandler(this.getFirstOriginCityDropdown());
        await this.getFirstOriginCityDropdown().click();
    }
    selectFirstDestinationCity = async () : Promise<void> => {
        await this.getFirstDestinationCitySelector().sendKeys('ZRH');
        browserWaitHandler(this.getFirstDestinationCityDropdown());
        await this.getFirstDestinationCityDropdown().click();
    }
    selectDepartureDate = async () : Promise<void> =>  {
        await this.getDepartureDateSelector().click();
        browserWaitHandler(element(by.css('.col-day.today')));
        await element(by.css('.col-day.today')).click();
    }
     selectFlightType = async () : Promise<void> => {
        await element(by.css('[id$=cabin_type0-select] option:nth-child(2)')).click();
    }
    selectDepartureTime = async () : Promise<void> => {
        await element(by.css('[id$=depart_time0-select] option:nth-child(1)')).click();
    }
}
