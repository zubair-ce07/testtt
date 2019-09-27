import { expect } from "chai";
import { browser } from "protractor";
import { FlightsPageMomondo } from "../../src/brands/momondo/pages/flights";
import { FlightsResultsPageMomondo } from "../../src/brands/momondo/pages/flightsResults";
import { MultiCityForm } from "../../src/core/elements/forms/multiCity";
import { TripType } from "../../src/core/elements/selectors/tripType";
import { DragHandle } from "../../src/core/elements/sliders/time";
import { FlightsPage } from "../../src/core/pages/flights";
import { FlightsResultsPage } from "../../src/core/pages/flightsResults";
import { formatDate } from "../../src/utils/specs.utils";

describe('Momondo Flights Search', () => {
  const Flights: FlightsPage = new FlightsPageMomondo();
  const FlightsResults: FlightsResultsPage = new FlightsResultsPageMomondo();
  
  const URL = `https://global.momondo.com`;
  const CABIN_TYPE = 'Business';
  const TRIP_TYPE = TripType.MULTI_CITY;
  const DATE_1 = new Date();
  const DATE_2 = new Date();
  const ORIGIN_1 = 'FRA';
  const ORIGIN_2 = 'ZRH';
  const DESTINATION_1 = 'ZRH';
  const DESTINATION_2 = 'LON';
  
  DATE_2.setDate(DATE_2.getDate() + 5);
  
  it(`should visit ${URL}`, async () => {
    browser.get(URL);
    expect(browser.getCurrentUrl()).eventually.to.contain(URL);
  });
  
  it('should set trip type to "multi-city"', async () => {
    const tripSelector = Flights.getTripSelector();
    await Flights.getTripSelector().select(TRIP_TYPE);
    expect(tripSelector.getCurrentTripType()).eventually.to.equal(TRIP_TYPE);
    expect(Flights.getMultiCityTripForm().getDisplayedLegsCount()).eventually.to.be.gte(2);
  });
  
  it('should set origin and destination for two flights', async () => {
    const multiCityTripForm: MultiCityForm = Flights.getMultiCityTripForm();
    const flightLeg1 = multiCityTripForm.getFlightSelector(0);
    const flightLeg2 = multiCityTripForm.getFlightSelector(1);
    
    await flightLeg1.setOrigin(ORIGIN_1);
    await flightLeg1.setDestination(DESTINATION_1);
    
    await flightLeg2.setOrigin(ORIGIN_2);
    await flightLeg2.setDestination(DESTINATION_2);
    
    expect(flightLeg1.getDisplayText('origin')).eventually.to.contain(ORIGIN_1);
    expect(flightLeg1.getDisplayText('destination')).eventually.to.contain(DESTINATION_1);
    expect(flightLeg2.getDisplayText('origin')).eventually.to.contain(ORIGIN_2);
    expect(flightLeg2.getDisplayText('destination')).eventually.to.contain(DESTINATION_2);
  });
  
  it('should set departure date for two flights', async () => {
    const dateSelector1 = Flights.getMultiCityTripForm().getDateSelector(0);
    const dateSelector2 = Flights.getMultiCityTripForm().getDateSelector(1);
    
    await dateSelector1.selectDate(DATE_1);
    expect(dateSelector1.getDisplayText()).eventually.to.equal(formatDate(DATE_1));
    
    await dateSelector2.selectDate(DATE_2);
    expect(dateSelector2.getDisplayText()).eventually.to.equal(formatDate(DATE_2));
  });
  
  it('should set cabin type to "Business" for two flights', async () => {
    const form = Flights.getMultiCityTripForm();
    
    const cabinSelector1 = form.getCabinSelector(0);
    await cabinSelector1.select(CABIN_TYPE);
    const cabinSelector2 = form.getCabinSelector(1);
    await cabinSelector2.select(CABIN_TYPE);
    
    expect(cabinSelector1.getDisplayText()).eventually.to.equal(CABIN_TYPE);
    expect(cabinSelector2.getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it('should click "Search" and load results page', async () => {
    await Flights.clickSearch().catch(error => {
      console.log(error.message);
    });
    
    expect(FlightsResults.getSearchResults().count()).eventually.to.greaterThan(0);
  });
  
  it('should contain two "time-off" sliders on search page', async () => {
    expect(FlightsResults.getTimeSliders().count()).eventually.to.be.equal(2);
    expect(FlightsResults.getTimeSlider(0).getDisplayText()).eventually.to.contain(ORIGIN_1);
    expect(FlightsResults.getTimeSlider(1).getDisplayText()).eventually.to.contain(ORIGIN_2);
  });
  
  
  it('should slide "time-off" slider and update results', async () => {
    await FlightsResults.getTimeSlider(0).drag(DragHandle.LEFT, 50);
    expect(FlightsResults.getSearchResults().count()).eventually.to.be.greaterThan(0);
    
    await FlightsResults.getTimeSlider(1).drag(DragHandle.LEFT, 50);
    expect(FlightsResults.getSearchResults().count()).eventually.to.be.greaterThan(0);
  });
  
  it('should open provider page when "view deal" is clicked', async () => {
    const flightResult = FlightsResults.getSearchResult(0);
    await flightResult.clickViewDeal();
    const windows = await browser.getAllWindowHandles();
    expect(windows.length).to.be.greaterThan(1);
  });
  
  it('should switch back to search results page', async () => {
    const windows = await browser.getAllWindowHandles();
    browser.switchTo().window(windows[0]);
    expect(browser.getCurrentUrl()).eventually.to.contain(URL);
  });
  
  it('should show correct values on search form', async () => {
    const form = FlightsResults.getMultiCityTripForm();
    await form.makeFormVisible();
    
    const flightSelector1 = form.getFlightSelector(0);
    const flightSelector2 = form.getFlightSelector(1);
    const dateSelector1 = form.getDateSelector(0);
    const dateSelector2 = form.getDateSelector(1);
    
    expect(flightSelector1.getDisplayText('origin')).eventually.to.contain(ORIGIN_1);
    expect(flightSelector2.getDisplayText('origin')).eventually.to.contain(ORIGIN_2);
    expect(flightSelector1.getDisplayText('destination')).eventually.to.contain(DESTINATION_1);
    expect(flightSelector2.getDisplayText('destination')).eventually.to.contain(DESTINATION_2);
    expect(form.getCabinSelector(0).getDisplayText()).eventually.to.equal(CABIN_TYPE);
    expect(form.getCabinSelector(1).getDisplayText()).eventually.to.equal(CABIN_TYPE);
    expect(dateSelector1.getDisplayText()).eventually.to.equal(formatDate(DATE_1));
    expect(dateSelector2.getDisplayText()).eventually.to.equal(formatDate(DATE_2));
  });
  
  it('should clear flight legs', async () => {
    await FlightsResults.getMultiCityTripForm().clearAll();
    const form = FlightsResults.getMultiCityTripForm();
    const flightSelector1 = form.getFlightSelector(0);
    const flightSelector2 = form.getFlightSelector(1);
    
    expect(flightSelector1.getDisplayText('origin')).eventually.to.not.contain(ORIGIN_1);
    expect(flightSelector2.getDisplayText('origin')).eventually.to.not.contain(ORIGIN_2);
    expect(flightSelector1.getDisplayText('destination')).eventually.to.not.contain(DESTINATION_1);
    expect(flightSelector2.getDisplayText('destination')).eventually.to.not.contain(DESTINATION_2);
    
    expect(form.getCabinSelector(0).getDisplayText()).eventually.to.equal(CABIN_TYPE);
    expect(form.getCabinSelector(1).getDisplayText()).eventually.to.equal(CABIN_TYPE);
  });
  
  it('should open error dialog when "search" is clicked', async () => {
    await FlightsResults.getMultiCityTripForm().clickSearch();
    expect(FlightsResults.getErrorDialog().isDisplayed()).eventually.to.be.true;
    expect(await FlightsResults.getErrorDialog().getErrorMessages()).length.greaterThan(0);
  });
  
  it('should close error dialog when "okay" is clicked', async () => {
    await FlightsResults.getErrorDialog().clickOkay();
    expect(FlightsResults.getErrorDialog().isDisplayed()).eventually.to.be.false;
  });
  
});
