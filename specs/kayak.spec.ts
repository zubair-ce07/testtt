import { browser } from "protractor";
import { expect, use } from "chai";
import chaiAsPromised from "chai-as-promised";
import { FlightsPage } from "../pages/Flights";
import { formatDate, removeNonNumericValues, toTimeString } from "../utils/specs.util";
import { FlightsResultsPage } from "../pages/FlightsResults";
import { switchToNewTabIfOpened } from "../utils/browser.util";
import { TripType } from "../components/Trip";
import { PassengerType } from "../components/Passenger";
import { FlightFilters } from "../components/Flights";

use(chaiAsPromised);

describe('Kayak.com', function () {
  beforeAll((done) => {
    browser.waitForAngularEnabled(false).then(() => done())
  });
  
  let flightsPage: FlightsPage;
  let flightsResultsPage: FlightsResultsPage;
  
  it('should open Kayak.com', async () => {
    flightsPage = new FlightsPage();
    await flightsPage.load();
    
    expect(flightsPage.form.origin.getDialog().isPresent()).eventually.to.be.true;
    expect(flightsPage.form.destination.getDialog().isPresent()).eventually.to.be.true;
    expect(flightsPage.form.dateRange.getDepartureDateDisplayValue()).eventually.to.be.not.null;
    expect(flightsPage.form.dateRange.getReturnDateDisplayValue()).eventually.to.be.not.null;
    expect(flightsPage.form.trip.value()).eventually.to.equal('Round-trip');
  });
  
  it('should switch to "one-way" trip-type mode', async () => {
    await flightsPage.form.trip.select(TripType.OneWay);
    expect(flightsPage.form.trip.value()).eventually.to.equal('One-way');
  });
  
  it('should switch to "multi-city" trip-type mode', async () => {
    await flightsPage.form.trip.select(TripType.MultiCity);
    expect(flightsPage.form.trip.value()).eventually.to.equal('Multi-city');
  });
  
  it('should switch to "round-trip" trip-type mode', async () => {
    await flightsPage.form.trip.select(TripType.RoundTrip);
    expect(flightsPage.form.trip.value()).eventually.to.equal('Round-trip');
  });
  
  it('should set 9 adults in passengers field', async () => {
    await flightsPage.form.passengers.openDialogWindow();
    await flightsPage.form.passengers.increment(PassengerType.Adults, 9);
    expect(flightsPage.form.passengers.errorMessage()).eventually.to.equal('Searches cannot have more than 9 adults');
    await flightsPage.form.passengers.closeDialogWindow();
  });
  
  it('should type "PAR" in origin and select first result', async () => {
    await flightsPage.form.origin.type('PAR');
    await flightsPage.form.origin.select(1);
    expect(flightsPage.form.origin.getSelectedValue()).eventually.to.equal('Paris (PAR)');
  });
  
  it('should type "NYC" in destination and select first result', async () => {
    await flightsPage.form.destination.type('NYC');
    await flightsPage.form.destination.select(1);
    expect(flightsPage.form.destination.getSelectedValue()).eventually.to.equal('New York (NYC)');
  });
  
  it('should set 4 adults in passengers field', async () => {
    await flightsPage.form.passengers.set(PassengerType.Adults, 4);
    expect(flightsPage.form.passengers.value()).eventually.to.equal('4 Travelers');
  });
  
  it('should set 2 children in passengers field', async () => {
    await flightsPage.form.passengers.set(PassengerType.Child, 2);
    await flightsPage.form.passengers.closeDialogWindow();
    expect(flightsPage.form.passengers.value()).eventually.to.equal('6 Travelers');
  });
  
  it('should set departure and arrival date', async () => {
    await flightsPage.form.dateRange.openDialogWindow();
    
    const date = new Date();
    const currentDate = new Date(`${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`);
    const departureDate = new Date(currentDate.setDate(currentDate.getDate() + 3));
    const returnDate = new Date(currentDate.setDate(currentDate.getDate() + 6));
    await flightsPage.form.dateRange.selectDate(departureDate, returnDate);
    
    expect(flightsPage.form.dateRange.getDepartureDateDisplayValue())
      .eventually.to.equal(formatDate(departureDate));
    
    expect(flightsPage.form.dateRange.getReturnDateDisplayValue())
      .eventually.to.equal(formatDate(returnDate));
  });
  
  it('should un-select all compare-to options by clicking "none"', async () => {
    await flightsPage.form.compare.selectNone();
  });
  
  it('should click search button and load flight search page', async () => {
    flightsResultsPage = await flightsPage.form.submit();
    await switchToNewTabIfOpened();
    await flightsResultsPage.load();
    await flightsResultsPage.dialog.closeIfOpen();
    expect(browser.getCurrentUrl()).eventually.to.contain('flights')
  });
  
  it('should display correctly filled search form', function () {
    const date = new Date();
    const currentDate = new Date(`${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`);
    const departureDate = new Date(currentDate.setDate(currentDate.getDate() + 3));
    const returnDate = new Date(currentDate.setDate(currentDate.getDate() + 6));
    
    expect(flightsResultsPage.form.trip.value()).eventually.to.equal('Round-trip');
    expect(flightsResultsPage.form.passengers.value()).eventually.to.equal('6 Travelers');
    expect(flightsResultsPage.form.dateRange.getReturnDateDisplayValue()).eventually.to.equal(formatDate(returnDate));
    expect(flightsResultsPage.form.dateRange.getDepartureDateDisplayValue()).eventually.to.equal(formatDate(departureDate));
  });
  
  it('should show least price in slowest sort option than other options', async () => {
    const cheapestPrice: any = await flightsResultsPage.header.getCost(FlightFilters.Cheapest).then(removeNonNumericValues);
    const bestPrice: any = await flightsResultsPage.header.getCost(FlightFilters.Best).then(removeNonNumericValues);
    expect(Number(cheapestPrice)).to.be.lte(Number(bestPrice));
  });
  
  it('should show least time in quickest sort option than other options', async () => {
    const quickestTime = await flightsResultsPage.header.getDuration(FlightFilters.Quickest).then(toTimeString);
    const slowestTime = await flightsResultsPage.header.getDuration(FlightFilters.Cheapest).then(toTimeString);
    expect(Date.parse(`01/01/1990 ${quickestTime}`)).to.be.lte(Date.parse(`01/01/1990 ${slowestTime}`));
  });
  
});
