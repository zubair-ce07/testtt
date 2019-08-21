import { IFlight } from '../core/interfaces/flight';
import { expect } from 'chai';
import { browser, by, element } from 'protractor';

describe(`${browser.params.brand} app assignment`, () => {
    const { flightPage } : { flightPage : IFlight} = browser.params;
    before( async () => {
        await browser.get(browser.baseUrl);
    });
    it('should select multiselect option' , async () => {
    await flightPage.selectMultiCity();
    expect(await flightPage.getMultiCitySection().isDisplayed()).to.be.true;
   });
    it('should type text in first origin city' , async () => {
     await flightPage.selectFirstOriginCity();
     expect(await flightPage.getFirstOriginCitySelectorValue()).to.be.equal('FRA');
    });
    it('should type text in first destination city' , async () => {
      await flightPage.selectFirstDestinationCity();
      expect(await flightPage.getFirstDestinationCitySelectorValue()).to.be.equal('ZRH');
    });
    it('should select departure date' , async () => {
       await flightPage.selectDepartureDate();
       expect(await flightPage.getDepartureDateSelector().getText()).to.equal('Wed 8/21');
    });
    it('should select the flight depature time' , async () => {
        await flightPage.selectDepartureTime();
        expect(await flightPage.getDepartureTimeSelector().getAttribute('value')).to.be.equal('a');
    });
    it('should select the flight type' , async () => {
        await flightPage.selectFlightType();
        expect(await element(by.css('[id$=cabin_type0-select]')).getAttribute('value')).to.be.equal('b');
    });
});
