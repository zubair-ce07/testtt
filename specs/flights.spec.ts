import { expect } from "chai";
import { browser } from "protractor";
import { TripType } from "../src/core/elements/selectors/tripType";
import { DragHandle } from "../src/core/elements/sliders/time";
import { BrandPagesFactory } from "../src/factory/brand";
import { formatDate } from "../src/utils/specs.utils";

const BRAND_NAME = process.env.RUN_TESTS_FOR_BRAND;
const {flightsPage, flightsResultsPage} = BrandPagesFactory.getPages(BRAND_NAME);

describe(`${BRAND_NAME} Flights Search`, () => {
  
  const URL = flightsPage.getURL();
  const CABIN_TYPE = 'Business';
  const TRIP_TYPE = TripType.MULTI_CITY;
  const DATE_1 = new Date();
  const DATE_2 = new Date();
  const ORIGIN_1 = 'FRA';
  const ORIGIN_2 = 'ZRH';
  const DESTINATION_1 = 'ZRH';
  const DESTINATION_2 = 'LON';
  
  DATE_2.setDate(DATE_2.getDate() + 5);
  
  it(`should visit "Flights" page`, async () => {
    await browser.get(URL);
    expect(browser.getCurrentUrl()).eventually.to.contain(URL);
  });
  
  it(`should set trip type to "${TRIP_TYPE}"`, async () => {
    const tripSelector = flightsPage.getTripSelector();
    await flightsPage.getTripSelector().select(TRIP_TYPE);
    expect(tripSelector.getCurrentTripType()).eventually.to.equal(TRIP_TYPE)
  });
  
  it('should show at least two flight legs on multi-city flight form', async () => {
    expect(flightsPage.getMultiCityTripForm().getDisplayedLegsCount()).eventually.to.be.gte(2);
  });
  
  it(`should set origin to "${ORIGIN_1}" of flight 1`, async () => {
    const flightSelector = flightsPage.getMultiCityTripForm().getFlightSelector(0);
    await flightSelector.setOrigin(ORIGIN_1);
    expect(flightSelector.getDisplayText('origin')).eventually.to.contain(ORIGIN_1);
  });
  
  it(`should set destination to "${DESTINATION_1}" of flight 1`, async () => {
    const flightSelector = flightsPage.getMultiCityTripForm().getFlightSelector(0);
    await flightSelector.setOrigin(DESTINATION_1);
    expect(flightSelector.getDisplayText('destination')).eventually.to.contain(DESTINATION_1);
  });
  
  it(`should set origin to "${ORIGIN_2}" of flight 2`, async () => {
    const flightSelector = flightsPage.getMultiCityTripForm().getFlightSelector(1);
    await flightSelector.setOrigin(ORIGIN_2);
    expect(flightSelector.getDisplayText('origin')).eventually.to.contain(ORIGIN_2);
  });
  
  it(`should set destination to "${DESTINATION_2}" of flight 2`, async () => {
    const flightSelector = flightsPage.getMultiCityTripForm().getFlightSelector(1);
    await flightSelector.setOrigin(DESTINATION_2);
    expect(flightSelector.getDisplayText('destination')).eventually.to.contain(DESTINATION_2);
  });
  
  it(`should set departure date as "${DATE_1.toDateString()}" for flight 1`, async () => {
    const dateSelector = flightsPage.getMultiCityTripForm().getDateSelector(0);
    await dateSelector.selectDate(DATE_1);
    expect(dateSelector.getDisplayText()).eventually.to.equal(formatDate(DATE_1));
  });
  
  it(`should set departure date as "${DATE_2.toDateString()}" for flight 2`, async () => {
    const dateSelector = flightsPage.getMultiCityTripForm().getDateSelector(0);
    await dateSelector.selectDate(DATE_1);
    expect(dateSelector.getDisplayText()).eventually.to.equal(formatDate(DATE_1));
  });
  
  it(`should set cabin type to "${CABIN_TYPE}" of flight 1`, async () => {
    const cabinSelector = flightsPage.getMultiCityTripForm().getCabinSelector(0);
    await cabinSelector.select(CABIN_TYPE);
    expect(cabinSelector.getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it(`should set cabin type to "${CABIN_TYPE}" of flight 2`, async () => {
    const cabinSelector = flightsPage.getMultiCityTripForm().getCabinSelector(1);
    await cabinSelector.select(CABIN_TYPE);
    expect(cabinSelector.getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it(`should click "Search" and load results page`, async () => {
    await flightsPage.clickSearch();
    expect(flightsResultsPage.getSearchResults().count()).eventually.to.greaterThan(0);
  });
  
  it(`should contain two "time-off" sliders on search page`, async () => {
    expect(flightsResultsPage.getTimeSliders().count()).eventually.to.be.equal(2);
  });
  
  it(`should contain "${ORIGIN_1}" in first time-slider display text`, async () => {
    expect(flightsResultsPage.getTimeSlider(0).getDisplayText()).eventually.to.contain(ORIGIN_1);
  });
  
  it(`should contain "${ORIGIN_2}" in second time-slider display text`, async () => {
    expect(flightsResultsPage.getTimeSlider(1).getDisplayText()).eventually.to.contain(ORIGIN_2);
  });
  
  it('should update results when first "time-off" slider is dragged', async () => {
    await flightsResultsPage.getTimeSlider(0).drag(DragHandle.LEFT, 50);
    expect(flightsResultsPage.getSearchResults().count()).eventually.to.be.greaterThan(0);
  });
  
  it('should update results when second "time-off" slider is dragged', async () => {
    await flightsResultsPage.getTimeSlider(1).drag(DragHandle.LEFT, 50);
    expect(flightsResultsPage.getSearchResults().count()).eventually.to.be.greaterThan(0);
  });
  
  it('should open provider page when "view deal" is clicked', async () => {
    const flightResult = flightsResultsPage.getSearchResult(0);
    await flightResult.clickViewDeal();
    const windows = await browser.getAllWindowHandles();
    expect(windows.length).to.be.greaterThan(1);
  });
  
  it('should switch back to search results page', async () => {
    const windows = await browser.getAllWindowHandles();
    browser.switchTo().window(windows[0]);
    expect(browser.getCurrentUrl()).eventually.to.contain(URL);
  });
  
  it('should show search form', async () => {
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.isFormVisible()).eventually.to.be.false;
    await form.makeFormVisible();
    expect(form.isFormVisible()).eventually.to.be.true;
  });
  
  it('should show correct origin on flight 1', async () => {
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.getFlightSelector(0).getDisplayText('origin')).eventually.to.contain(ORIGIN_1);
  });
  
  it('should show correct origin on flight 2', async () => {
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.getFlightSelector(1).getDisplayText('origin')).eventually.to.contain(ORIGIN_2);
  });
  
  it('should show correct destination on flight 1', async () => {
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.getFlightSelector(0).getDisplayText('destination')).eventually.to.contain(DESTINATION_1);
  });
  
  it('should show correct destination on flight 2', async () => {
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.getFlightSelector(0).getDisplayText('destination')).eventually.to.contain(DESTINATION_2);
  });
  
  it('should show correct date on flight 1', async () => {
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.getDateSelector(0).getDisplayText()).eventually.to.equal(formatDate(DATE_1));
  });
  
  it('should show correct date on flight 2', async () => {
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.getDateSelector(1).getDisplayText()).eventually.to.equal(formatDate(DATE_2));
  });
  
  it('should show correct cabin type on flight 1', async () => {
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.getCabinSelector(0).getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it('should show correct cabin type on flight 2', async () => {
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.getCabinSelector(1).getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it('should clear flight legs', async () => {
    await flightsResultsPage.getMultiCityTripForm().clearAll();
    const form = flightsResultsPage.getMultiCityTripForm();
    expect(form.isFormVisible()).eventually.to.be.true;
  });
  
  it(`should clear "${ORIGIN_1}" in  flight 1 origin`, async () => {
    const flightSelector = flightsResultsPage.getMultiCityTripForm().getFlightSelector(0);
    expect(flightSelector.getDisplayText('origin')).eventually.to.not.contain(ORIGIN_1);
  });
  
  it(`should clear "${DESTINATION_1}" in  flight 1 destination`, async () => {
    const flightSelector = flightsResultsPage.getMultiCityTripForm().getFlightSelector(0);
    expect(flightSelector.getDisplayText('destination')).eventually.to.not.contain(DESTINATION_1);
  });
  
  it(`should clear "${ORIGIN_2}" in  flight 2 origin`, async () => {
    const flightSelector = flightsResultsPage.getMultiCityTripForm().getFlightSelector(1);
    expect(flightSelector.getDisplayText('origin')).eventually.to.not.contain(ORIGIN_2);
  });
  
  it(`should clear "${DESTINATION_2}" in  flight 2 destination`, async () => {
    const flightSelector = flightsResultsPage.getMultiCityTripForm().getFlightSelector(1);
    expect(flightSelector.getDisplayText('destination')).eventually.to.not.contain(DESTINATION_2);
  });
  
  it(`should still show cabin type as "${CABIN_TYPE}" on flight 1`, async () => {
    expect(flightsPage.getMultiCityTripForm().getCabinSelector(0).getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it(`should still show cabin type as "${CABIN_TYPE}" on flight 2`, async () => {
    expect(flightsPage.getMultiCityTripForm().getCabinSelector(1).getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it('should open error dialog when "search" is clicked', async () => {
    await flightsResultsPage.getMultiCityTripForm().clickSearch();
    expect(flightsResultsPage.getErrorDialog().isDisplayed(), 'error should be visible').eventually.to.be.true;
  });
  
  it('should contain at least 2 messages in error dialog', async () => {
    expect(await flightsResultsPage.getErrorDialog().getErrorMessages()).length.greaterThan(2);
  });
  
  it('should close error dialog when "okay" is clicked', async () => {
    await flightsResultsPage.getErrorDialog().clickOkay();
    expect(flightsResultsPage.getErrorDialog().isDisplayed()).eventually.to.be.false;
  });
  
});
