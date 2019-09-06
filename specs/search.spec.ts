import { browser }                from 'protractor';
import { use }                    from 'chai';
import chaiAsPromised             from "chai-as-promised";
import { parse }                  from "../utils/scenario.util";
import { all, getAirportCode }    from "../utils/specs.util";
import { LandingPage }            from "../pages/Flights";
import { switchToNewTabIfOpened } from "../utils/browser.util";
import { FlightsResultsPage }     from "../pages/FlightsResults";

const scenarios = parse(require('../scenarios/search.scenario.json'));

use(chaiAsPromised);

describe('Flights Search Scenarios', () => {
  
  beforeAll((done) => {
    browser.waitForAngularEnabled(false).then(done);
  });
  
  let page: LandingPage;
  beforeEach(async (done) => {
    page = new LandingPage();
    await page.load();
    await page.searchForm.passengers.reset();
    done();
  });
  
  all(scenarios, (scenario) => {
    it(`${scenario.title}`, async function () {
      
      await page.searchForm.origin.type(scenario.origin.input);
      
      const originAirportCode = getAirportCode(scenario.origin.selection);
      browser.sleep(1000);
      await page.searchForm.origin.getSearchResults().then(async airports => {
        const idx = airports.findIndex(airport => airport.code == originAirportCode);
        browser.sleep(1000);
        await page.searchForm.origin.select(idx + 1);
      });
      
      await page.searchForm.destination.type(scenario.destination.input);
      const destinationAirportCode = getAirportCode(scenario.destination.selection);
      browser.sleep(2000);
      await page.searchForm.destination.getSearchResults().then(airports => {
        const idx = airports.findIndex(airport => airport.code == destinationAirportCode);
        browser.sleep(1000);
        return page.searchForm.destination.select(idx + 1);
      });
      
      for (const passenger of Object.keys(scenario.passengers)) {
        const value = scenario.passengers[passenger];
        await page.searchForm.passengers.set(passenger, value);
        browser.sleep(1000);
      }
      
      await page.searchForm.submit();
      
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
