import { expect } from "chai";
import { browser } from "protractor";
import { CabinType } from '../src/core/elements/selectors/cabinType';
import { TripType } from "../src/core/elements/selectors/tripType";
import { DragHandle } from "../src/core/elements/sliders/time";
import { FlightsPageFactory } from "../src/factory/flightsPage";
import { FlightsResultsPageFactory } from "../src/factory/flightsResultsPage";
import { addDays, formatDate } from "../src/utils/specs.utils";

const BRAND_NAME = process.env.RUN_TESTS_FOR_BRAND;

const flightsPage = new FlightsPageFactory().create(BRAND_NAME);
const flightsResultsPage = new FlightsResultsPageFactory().create(BRAND_NAME);

describe(`${BRAND_NAME} Flights Search`, () => {
  
  const URL = flightsPage.getURL();
  const CABIN_TYPE = CabinType.BUSINESS;
  const TRIP_TYPE = TripType.MULTI_CITY;
  const CURRENT_DATE = new Date();
  const CURRENT_DATE_PLUS_FIVE_DAYS = addDays(CURRENT_DATE, 5);
  const ORIGIN_1 = 'FRA';
  const ORIGIN_2 = 'ZRH';
  const DESTINATION_1 = 'ZRH';
  const DESTINATION_2 = 'LON';
  
  const multiCityTripForm = flightsPage.getMultiCityTripForm();
  
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
    expect(multiCityTripForm.getDisplayedLegsCount()).eventually.to.be.gte(2);
  });
  
  it(`should set origin to "${ORIGIN_1}" of flight 1`, async () => {
    const flightSelector = multiCityTripForm.getFlightSelector(0);
    await flightSelector.setOrigin(ORIGIN_1);
    expect(flightSelector.getDisplayText('origin')).eventually.to.contain(ORIGIN_1);
  });
  
  it(`should set destination to "${DESTINATION_1}" of flight 1`, async () => {
    const flightSelector = multiCityTripForm.getFlightSelector(0);
    await flightSelector.setOrigin(DESTINATION_1);
    expect(flightSelector.getDisplayText('destination')).eventually.to.contain(DESTINATION_1);
  });
  
  it(`should set origin to "${ORIGIN_2}" of flight 2`, async () => {
    const flightSelector = multiCityTripForm.getFlightSelector(1);
    await flightSelector.setOrigin(ORIGIN_2);
    expect(flightSelector.getDisplayText('origin')).eventually.to.contain(ORIGIN_2);
  });
  
  it(`should set destination to "${DESTINATION_2}" of flight 2`, async () => {
    const flightSelector = multiCityTripForm.getFlightSelector(1);
    await flightSelector.setOrigin(DESTINATION_2);
    expect(flightSelector.getDisplayText('destination')).eventually.to.contain(DESTINATION_2);
  });
  
  it(`should set departure date as "${CURRENT_DATE.toDateString()}" for flight 1`, async () => {
    const dateSelector = multiCityTripForm.getDateSelector(0);
    await dateSelector.selectDate(CURRENT_DATE);
    expect(dateSelector.getDisplayText()).eventually.to.equal(formatDate(CURRENT_DATE));
  });
  
  it(`should set departure date as "${CURRENT_DATE_PLUS_FIVE_DAYS.toDateString()}" for flight 2`, async () => {
    const dateSelector = multiCityTripForm.getDateSelector(0);
    await dateSelector.selectDate(CURRENT_DATE);
    expect(dateSelector.getDisplayText()).eventually.to.equal(formatDate(CURRENT_DATE));
  });
  
  it(`should set cabin type to "${CABIN_TYPE}" of flight 1`, async () => {
    const cabinSelector = multiCityTripForm.getCabinSelector(0);
    await cabinSelector.select(CABIN_TYPE);
    expect(cabinSelector.getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it(`should set cabin type to "${CABIN_TYPE}" of flight 2`, async () => {
    const cabinSelector = multiCityTripForm.getCabinSelector(1);
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
    expect(multiCityTripForm.isFormVisible()).eventually.to.be.false;
    await multiCityTripForm.makeFormVisible();
    expect(multiCityTripForm.isFormVisible()).eventually.to.be.true;
  });
  
  it('should show correct origin on flight 1', async () => {
    expect(multiCityTripForm.getFlightSelector(0).getDisplayText('origin')).eventually.to.contain(ORIGIN_1);
  });
  
  it('should show correct origin on flight 2', async () => {
    expect(multiCityTripForm.getFlightSelector(1).getDisplayText('origin')).eventually.to.contain(ORIGIN_2);
  });
  
  it('should show correct destination on flight 1', async () => {
    expect(multiCityTripForm.getFlightSelector(0).getDisplayText('destination')).eventually.to.contain(DESTINATION_1);
  });
  
  it('should show correct destination on flight 2', async () => {
    expect(multiCityTripForm.getFlightSelector(0).getDisplayText('destination')).eventually.to.contain(DESTINATION_2);
  });
  
  it('should show correct date on flight 1', async () => {
    expect(multiCityTripForm.getDateSelector(0).getDisplayText()).eventually.to.equal(formatDate(CURRENT_DATE));
  });
  
  it('should show correct date on flight 2', async () => {
    expect(multiCityTripForm.getDateSelector(1).getDisplayText()).eventually.to.equal(formatDate(CURRENT_DATE_PLUS_FIVE_DAYS));
  });
  
  it('should show correct cabin type on flight 1', async () => {
    expect(multiCityTripForm.getCabinSelector(0).getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it('should show correct cabin type on flight 2', async () => {
    expect(multiCityTripForm.getCabinSelector(1).getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it('should clear flight legs', async () => {
    await flightsResultsPage.getMultiCityTripForm().clearAll();
    expect(multiCityTripForm.isFormVisible()).eventually.to.be.true;
  });
  
  it(`should clear "${ORIGIN_1}" in  flight 1 origin`, async () => {
    expect(multiCityTripForm.getFlightSelector(0).getDisplayText('origin')).eventually.to.not.contain(ORIGIN_1);
  });
  
  it(`should clear "${DESTINATION_1}" in  flight 1 destination`, async () => {
    expect(multiCityTripForm.getFlightSelector(0).getDisplayText('destination')).eventually.to.not.contain(DESTINATION_1);
  });
  
  it(`should clear "${ORIGIN_2}" in  flight 2 origin`, async () => {
    expect(multiCityTripForm.getFlightSelector(1).getDisplayText('origin')).eventually.to.not.contain(ORIGIN_2);
  });
  
  it(`should clear "${DESTINATION_2}" in  flight 2 destination`, async () => {
    expect(multiCityTripForm.getFlightSelector(1).getDisplayText('destination')).eventually.to.not.contain(DESTINATION_2);
  });
  
  it(`should still show cabin type as "${CABIN_TYPE}" on flight 1`, async () => {
    expect(multiCityTripForm.getCabinSelector(0).getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it(`should still show cabin type as "${CABIN_TYPE}" on flight 2`, async () => {
    expect(multiCityTripForm.getCabinSelector(1).getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it('should open error dialog when "search" is clicked', async () => {
    await multiCityTripForm.clickSearch();
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
