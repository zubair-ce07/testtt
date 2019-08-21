import { ElementFinder, promise } from 'protractor';

export interface IConfig {
    url : string;
    brand : string;
    pageObject : IFlight;
}

export interface IFlight {
  selectMultiCity () : void;
  getFirstOriginCitySelectorValue () : Promise<string>;
  getFirstDestinationCitySelectorValue () : Promise<string>;
  getMultiCitySection () : ElementFinder;
  getFirstOriginCityDropdown () : ElementFinder;
  getFirstDestinationCityDropdown () : ElementFinder;
  getDepartureDateSelector () : ElementFinder;
  getDepartureTimeSelector () : ElementFinder;
  selectFirstOriginCity () : Promise<void>;
  selectFirstDestinationCity () : Promise<void>;
  selectDepartureDate () : Promise <void>;
  selectFlightType () : Promise <void>;
  selectDepartureTime () : Promise <void>;
}
