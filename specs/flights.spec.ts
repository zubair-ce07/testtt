import { expect } from "chai";
import { browser } from "protractor";
import { FlightsPage } from "../src/pages/flightsPage";
import { diffInDays, findCurrentLocation } from "../src/utils/specs.utils";
import { FlightsResultsPage } from "../src/pages/flightsResultsPage";
import { FlightsPageKayak } from "../src/brands/kayak/page/flightsPageKayak";
import { FlightsResultsPageKayak } from "../src/brands/kayak/page/flightsResultsPageKayak";

const flightsPage: FlightsPage = new FlightsPageKayak();
const flightsResultsPage: FlightsResultsPage = new FlightsResultsPageKayak();

describe(`Kayak SEM Flights Search`, () => {
  beforeAll(async (done) => {
    await flightsPage.visit();
    done();
  });
  
  it('should show "Find hotel deals" in h1 header', async () => {
    expect(await flightsPage.getHeaderText()).equal('Find hotel deals');
  });
  
  it('should show destination pre-filled by geo IP', async () => {
    const location = await findCurrentLocation();
    expect(await flightsPage.getSearchForm().getDestination().getDisplayText()).equal(location);
  });
  
  it('should show pre-selected dates, check-in date tomorrow with 1 night duration', async () => {
    const dateRange = flightsPage.getSearchForm().getDateRange();
    const startDate = await dateRange.getStartDateText();
    const endDate = await dateRange.getEndDateText();
    
    expect(diffInDays(startDate, endDate)).equal(1);
  });
  
  it('should show photo banner behind main search form', async () => {
    expect(await flightsPage.getSearchFormBanners().count()).be.greaterThan(0);
  });
  
  it('should show "Compare To" section when destination is filled', async () => {
    expect(await flightsPage.getSearchForm().getCompareTo().isDisplayed()).is.true;
  });
  
  it('should show no "Compare To" section while destination value is empty', async () => {
    await flightsPage.getSearchForm().getDestination().type('');
    expect(await flightsPage.getSearchForm().getCompareTo().isDisplayed()).is.false;
  });
  
  it('should show email subscription field', async () => {
    expect(await flightsPage.getSubscription().isDisplayed()).is.true;
  });
  
  it('should show 3 ad slots', async () => {
    expect(await flightsPage.getSlotAds().count()).equal(3);
  });
  
  it('should show tiles with links to flights', async () => {
    expect(await flightsPage.getTiles().count()).be.greaterThan(0);
  });
  
  it('should show worldwide, continent and country links', async () => {
    expect(await flightsPage.getDestinationSwitcher().getOptions()).length.greaterThan(0);
  });
  
  it('should show Find the perfect hotel section with search button', async () => {
    expect(await flightsPage.getSearchPromo().isDisplayed()).is.true;
  });
  
  it('should show mobile app section', async () => {
    expect(await flightsPage.getMobilePromo().isDisplayed()).is.true;
  });
  
  it('should set destination until compare to appear', async () => {
    const location = await findCurrentLocation();
    await flightsPage.getSearchForm().getDestination().type(location);
    expect(await flightsPage.getSearchForm().getCompareTo().isDisplayed()).is.true;
  });
  
  it('should select at least one compare to option if not selected already', async () => {
    const compareTo = flightsPage.getSearchForm().getCompareTo();
    await compareTo.selectAtLeast(1);
    expect(await compareTo.getSelected()).length.is.greaterThan(0);
  });
  
  it('should be able to perform search, and load results page', async () => {
    await flightsPage.search();
    expect(await flightsResultsPage.getSearchResults().count()).be.greaterThan(0);
  });
  
  it('should show correct data on results page', async () => {
    expect(await flightsResultsPage.getSearchResults().count()).be.greaterThan(0);
  });
  
  it('should return to SEM landing page', async () => {
    await flightsPage.visit();
    expect(await browser.getCurrentUrl()).is.equal(flightsPage.getURL());
  });
  
  it('should open hotels search overlay after clicking on hotels link in a tile', async () => {
    await flightsPage.getTile(0).triggerHotels();
    const dialog = flightsPage.getTilesHotelDialog();
    expect(await dialog.isDisplayed()).is.true;
    await dialog.close();
  });
  
  it('should select at least one compare to option if not selected already', async () => {
    const compareTo = flightsPage.getSearchForm().getCompareTo();
    await compareTo.selectAtLeast(1);
    expect(await compareTo.getSelected()).length.is.greaterThan(0);
  });
  
  it('should be able to perform search, and load results page', async () => {
    await flightsPage.search();
    expect(await flightsResultsPage.getSearchResults().count()).be.greaterThan(0);
  });
  
  it('should show correct data on results page', async () => {
    expect(await flightsResultsPage.getSearchResults().count()).be.greaterThan(0);
  });
  
  it('should return to SEM landing page', async () => {
    await flightsPage.visit();
    expect(await browser.getCurrentUrl()).is.equal(flightsPage.getURL());
  });
  
  it('should open flights search overlay after clicking on flights link in a tile', async () => {
    await flightsPage.getTile(0).triggerFlights();
    const dialog = flightsPage.getTilesFlightDialog();
    expect(await dialog.isDisplayed()).is.true;
    await dialog.close();
  });
  
  it('should select at least one compare to option if not selected already', async () => {
    const compareTo = flightsPage.getSearchForm().getCompareTo();
    await compareTo.selectAtLeast(1);
    expect(await compareTo.getSelected()).length.is.greaterThan(0);
  });
  
  it('should be able to perform search, and load results page', async () => {
    await flightsPage.search();
    expect(await flightsResultsPage.getSearchResults().count()).be.greaterThan(0);
  });
  
  it('should show correct data on results page', async () => {
    expect(await flightsResultsPage.getSearchResults().count()).be.greaterThan(0);
  });
  
  it('should return to SEM landing page', async () => {
    await flightsPage.visit();
    expect(await browser.getCurrentUrl()).is.equal(flightsPage.getURL());
  });
  
  it('should open hotels search overlay after clicking on "Search Now" in "Find the perfect hotel" section', async () => {
    await flightsPage.getSearchPromo().searchNow();
    expect(await flightsPage.getHotelsSearchDialog().isDisplayed()).is.true;
    await flightsPage.getHotelsSearchDialog().close();
  });
  
  it('should select at least one compare to option if not selected already', async () => {
    const compareTo = flightsPage.getSearchForm().getCompareTo();
    await compareTo.selectAtLeast(1);
    expect(await compareTo.getSelected()).length.is.greaterThan(0);
  });
  
  it('should be able to perform search, and load results page', async () => {
    await flightsPage.search();
    expect(await flightsResultsPage.getSearchResults().count()).be.greaterThan(0);
  });
  
  it('should show correct data on results page', async () => {
    expect(await flightsResultsPage.getSearchResults().count()).be.greaterThan(0);
  });
});
