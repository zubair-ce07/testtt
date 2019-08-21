import { Aliases } from './../conf/config';
import { IFlight } from './../core/interfaces/flight';
import { by, element, ElementFinder, Key } from 'protractor';
import { browserWaitHandler } from '../core/utils';
import { async } from 'q';
export class MomondoFlightsPageObject implements IFlight {
    selectMultiCity = () : void  => {
        element.all(by.css('[id$=multicity-label]')).first().click();
    }
    getMultiCitySection = () : ElementFinder => element(by.css('[id$=multi-fields]'));
    getFirstOriginCitySelector = () : ElementFinder => element(by.css('input[id$=origin0]'));
    getFirstOriginCityDropdown = () => element(by.css('[id$=origin0-smartbox-dropdown] ul li:first-child'));
    getFirstDestinationCityDropdown = () => element(by.css('[id$=destination0-smartbox-dropdown] ul li:first-child'));
    getFirstDestinationCitySelector = () : ElementFinder => element(by.css('input[id$=destination0]'));
    getDepartureDateSelector = () : ElementFinder => element(by.css('[id$=departDate0-input]'));
    getDepartureTimeSelector = () : ElementFinder => element(by.css('[id$=depart_time0-select]'));
    selectFlightTypeSelector = () : ElementFinder => element(by.css('[id$=cabin_type0-select]'));
    getFirstOriginCitySelectorValue = async () => element(by.css('input[id$=origin0]')).getAttribute('value');
    getFirstDestinationCitySelectorValue = async () => element(by.css('input[id$=destination0]')).getAttribute('value');
    selectFirstOriginCity = async () : Promise<void> => {
        this.getFirstOriginCitySelector().sendKeys(Key.chord(Key.CONTROL, 'a', Key.DELETE));
        await this.getFirstOriginCitySelector().sendKeys(Aliases.FirstOriginInput);
        browserWaitHandler(this.getFirstOriginCityDropdown());
        await this.getFirstOriginCityDropdown().click();
    }
    selectFirstDestinationCity = async () : Promise<void> => {
        await this.getFirstDestinationCitySelector().sendKeys(Aliases.FirstOriginInput);
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
