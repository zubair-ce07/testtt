import { browser } from 'protractor';
import { use } from 'chai';
import chaiAsPromised from "chai-as-promised";
import { parse } from "../utils/scenario.util";
import { all, getAirportCode } from "../utils/specs.util";
import { FlightsPage } from "../pages/Flights";
import { switchToNewTabIfOpened } from "../utils/browser.util";
import { FlightsResultsPage } from "../pages/FlightsResults";

const scenarios = parse(require('../scenarios/search.scenario.json'));

use(chaiAsPromised);

describe('Flights Search Scenarios', () => {
  
  beforeAll((done) => {
    browser.waitForAngularEnabled(false).then(done);
  });
  
  let flightsPage: FlightsPage;
  beforeEach(async (done) => {
    flightsPage = new FlightsPage();
    await flightsPage.load();
    done();
  });
  
  all(scenarios, (scenario) => {
    it(`${scenario.title}`, async () => {
      await flightsPage.form.origin.type(scenario.origin.input);
      
      const originAirportCode = getAirportCode(scenario.origin.selection);
      browser.sleep(1000);
      await flightsPage.form.origin.getSearchResults().then(async airports => {
        const idx = airports.findIndex(airport => airport.code == originAirportCode);
        browser.sleep(1000);
        await flightsPage.form.origin.select(idx + 1);
      });
    
      await flightsPage.form.destination.type(scenario.destination.input);
      const destinationAirportCode = getAirportCode(scenario.destination.selection);
      browser.sleep(2000);
      await flightsPage.form.destination.getSearchResults().then(airports => {
        const idx = airports.findIndex(airport => airport.code == destinationAirportCode);
        browser.sleep(1000);
        return flightsPage.form.destination.select(idx + 1);
      });
      
      for (const passenger of Object.keys(scenario.passengers)) {
        const value = scenario.passengers[passenger];
        await flightsPage.form.passengers.set(passenger, value);
        browser.sleep(1000);
      }
    
      await flightsPage.form.submit();
      
      await switchToNewTabIfOpened();
      
      const results = new FlightsResultsPage(await browser.getCurrentUrl());
      await results.load();
      await results.dialog.closeIfOpen();
    }, 60 * 1000);
  });
  
  afterEach(() => {
    browser.executeScript(() => {
      window.localStorage.clear();
      window.sessionStorage.clear();
    })
  });
  
});
