import { MomondoFlightsPageObject } from './../page-objects/momondo-flight.page';
import { KayakFlightsPageObject } from './../page-objects/kayak-filght.page';
import { IConfig } from '../core/interfaces/flight';

export const configArray : Array<IConfig>  = [
     {
       url : 'https://www.kayak.com',
       brand :  'kayak',
       pageObject : new KayakFlightsPageObject(),
     },
     {
        url : 'https://www.momondo.com',
        brand :  'momondo',
        pageObject : new MomondoFlightsPageObject(),
      },
];

export const Aliases = {
  FirstOriginInput : 'FRA',
  FirstDestinationInput : 'ZRH',
};
