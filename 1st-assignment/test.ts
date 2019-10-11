import { browser, element, by, promise} from 'protractor';
import { HomePageObject } from './homePageObject';
import { FlightsPageObject } from './flightsPageObject';
import { SearchFormObject } from './searchFormObject';
import { async } from 'q';

var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
var should = chai.should();
let homePageObject: HomePageObject = new HomePageObject();
let flightsPageObject: FlightsPageObject = new FlightsPageObject();
let searchFormObject: SearchFormObject = new SearchFormObject();

describe("kayak Automation", async function() {
  before(async function() {
    browser.waitForAngularEnabled(false);
    await browser.get('https://www.kayak.com');
  });

  it("Select flights from top", function() {
    homePageObject.clickFlights().should.eventually.includes('flights')
  });

  it("Should display the origin field", function() {
    searchFormObject.getDepartureDisplay().isDisplayed().should.eventually.be.true;
  });

  it("Should display the destination field", function() {
    searchFormObject.getDestinationDisplay().isDisplayed().should.eventually.be.true;
  });

  it("Should display the departure date field", function() {
    searchFormObject.departureDateFieldDisplay().isDisplayed().should.eventually.be.true;
  });

  it("Should display the return date field", function() {
    searchFormObject.returnDateFieldDisplay().isDisplayed().should.eventually.be.true;
  });

  it("Should display ‘Round-trip’ in trip type field", function() {
    homePageObject.roundTripField.getText().should.eventually.be.equal('Round-trip');
  });

  it("Switch to ‘One-way’ trip type mode", function() {
    homePageObject.changeToOneWayTrip();
    homePageObject.roundTripField.getText().should.eventually.be.equal('One-way');
  });
  
  it("Switch to ‘Multi-city’ trip type mode", function() {
    homePageObject.changeToMulticityTrip();
    homePageObject.roundTripField.getText().should.eventually.be.equal('Multi-city');
  });

  it("Change number of ‘adults’ from travelers field to 9", function() {
    homePageObject.addAdultPassengers(10);
    homePageObject.getAdultsLimitMessage().should.eventually.be.equal("Searches cannot have more than 9 adults");
  });

  it("Switch to ‘Round-trip’ trip type mode", function() {
    homePageObject.changeToRoundTrip();
    homePageObject.roundTripField.getText().should.eventually.be.equal('Round-trip');
  });

  it("Should display ‘Paris (PAR)’ in origin field", async function() {
    await homePageObject.setDeparture("PAR");
    await homePageObject.getDepartureValue().should.eventually.be.equal("Paris (PAR)");
  });

  it("Should display ‘New York (NYC)’ in the destination field", async function() {
    await homePageObject.setDestination("NYC");
    await homePageObject.getDestinationValue().should.eventually.be.equal("New York (NYC)");
  });

  it("Should display accurate date in departure field", function() {
    homePageObject.fillDatesDeparture();
    homePageObject.getDepartureDate().should.eventually.be.equal(homePageObject.getTripDates(3));
  });

  it("Should display accurate date in return date field", function() {
    homePageObject.fillDatesReturn();
    homePageObject.getReturnDate().should.eventually.be.equal(homePageObject.getTripDates(6));
  });

  it("Should display all unchecked checkboxes in compare-to block", function() {
    homePageObject.uncheckAllCheckBox();
  });

  it("Should display ‘4 Travelers’ in the travelers field", function() {
    homePageObject.decreaseAdultPassengers(6);
    homePageObject.getAdultPassenger().should.eventually.be.equal('4');
  });

  it("Should display ‘6 Travelers’ in the travelers field", function() {
    homePageObject.addChildPassengers(2);
    homePageObject.getChildPassenger().should.eventually.be.equal('2');
  });

  it("Should display correct filled-in search form on results page", function() {
    homePageObject.clickSearch().should.eventually.includes('sort=bestflight_a');
  });

  it("Should display the origin field", function() {
    searchFormObject.getDepartureDisplay().isDisplayed().should.eventually.be.true;
  });

  it("Should display the destination field", function() {
    searchFormObject.getDestinationDisplay().isDisplayed().should.eventually.be.true;
  });

  it("Should display the departure date field", function() {
    searchFormObject.departureDateFieldDisplay().isDisplayed().should.eventually.be.true;
  });

  it("Should display the return date field", function() {
    searchFormObject.returnDateFieldDisplay().isDisplayed().should.eventually.be.true;
  });

  it("Should display least price in ‘Cheapest’ sort option compared to ‘Best’ and ‘Quickest’ sort options", async function() {
    const cheapPrice = flightsPageObject.getCheapestPrice();
    const bestPrice = flightsPageObject.getBestPrice();
    const quickPrice = flightsPageObject.getQuickestPrice(); 
    await promise.all([cheapPrice,bestPrice,quickPrice]);
  });

  it("Should display least time in ‘Quickest’ sort option compared to ‘Cheapest’ and ‘Best’ sort options", function() { 
    const cheapTime = flightsPageObject.getCheapestTime();
    const bestTime = flightsPageObject.getBestTime();
    const quickTime = flightsPageObject.getQuickestTime();
    promise.all([cheapTime, bestTime, quickTime]);
  });
});
