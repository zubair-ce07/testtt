import { browser, element, by, promise} from 'protractor';
import { HomePageObject } from './homePageObject';
import { FlightsPageObject } from './flightsPageObject';
import { SearchFormObject } from './searchFormObject';

var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
var should = chai.should();
let homePageObject: HomePageObject = new HomePageObject();
let flightsPageObject: FlightsPageObject = new FlightsPageObject();
let searchFormObject: SearchFormObject = new SearchFormObject();

describe("kayak Automation", async function() {
  before(function() {
    browser.waitForAngularEnabled(false);
    browser.get('https://www.kayak.com');
    browser.manage().deleteAllCookies();
  });

  it("Select flights from top", async function() {
    const url = await homePageObject.clickFlights();
    url.includes('flights');
  });

  // it("Should display the origin field", async function() {
  //   searchFormObject.getDepartureDisplay().should.eventually.be.equal(true);
  // });

  // it("Should display the destination field", async function() {
  //   await searchFormObject.getDestinationDisplay().should.eventually.be.equal(true);
  // });

  // it("Should display the departure date field", async function() {
  //   await searchFormObject.departureDateFieldDisplay().should.eventually.be.equal(true);
  // });

  // it("Should display the return date field", async function() {
  //   await searchFormObject.returnDateFieldDisplay().should.eventually.be.equal(true);
  // });

  // it("Should display ‘Round-trip’ in trip type field", async function() {
  //   await homePageObject.roundTripTypeField().should.eventually.be.equal(true);
  // });

  // it("Switch to ‘One-way’ trip type mode", async function() {
  //   homePageObject.changeToOneWayTrip();
  //   await searchFormObject.departureDateFieldDisplay().should.eventually.be.equal(true);
  // });
  
  // it("Switch to ‘Multi-city’ trip type mode", async function() {
  //   homePageObject.changeToMulticityTrip();
  //   await homePageObject.multiCities().should.eventually.be.equal(true);
  // });

  // it("Switch to ‘Round-trip’ trip type mode", async function() {
  //   homePageObject.changeToRoundTrip();
  //   await searchFormObject.returnDateFieldDisplay().should.eventually.be.equal(true);
  // });

  // it("Change number of ‘adults’ from travelers field to 9", async function() {
  //   await homePageObject.addAdultPassengers(10);
  //   await homePageObject.getAdultsLimitMessage().should.eventually.be.equal("Searches cannot have more than 9 adults");
  // });

  it("Should display ‘Paris (PAR)’ in origin field", async function() {
    await homePageObject.setDeparture("PAR");
    await homePageObject.getDepartureValue().should.eventually.be.equal("Paris (PAR)");
  });

  it("Should display ‘New York (NYC)’ in the destination field", async function() {
    await homePageObject.setDestination("NYC");
    await homePageObject.getDestinationValue().should.eventually.be.equal("New York (NYC)");
  });

  it("Should display accurate date in departure field", async function() {
    await homePageObject.fillDatesDeparture();
    homePageObject.getDepartureDate().should.eventually.be.equal(homePageObject.getTripDates(3));
  });

  it("Should display accurate date in return date field", async function() {
    await homePageObject.fillDatesReturn();
    homePageObject.getReturnDate().should.eventually.be.equal(homePageObject.getTripDates(6));
  });

  it("Should display all unchecked checkboxes in compare-to block", function() {
    homePageObject.uncheckAllCheckBox();
  });

  // it("Should display ‘4 Travelers’ in the travelers field", async function() {
  //   homePageObject.decreaseAdultPassengers(6);
  //   await homePageObject.getAdultPassenger().should.eventually.be.equal(4);
  // });

  // it("Should display ‘6 Travelers’ in the travelers field", async function() {
  //   homePageObject.addChildPassengers(2);
  //   await homePageObject.getChildPassenger().should.eventually.be.equal(2);
  // });

  it("Should display correct filled-in search form on results page", async function() {
    await homePageObject.clickSearch().should.eventually.be.includes('sort=bestflight_a');
  });

  it("Should display the origin field", async function() {
    searchFormObject.getDepartureDisplay().should.eventually.be.equal(true);
  });

  it("Should display the destination field", async function() {
    await searchFormObject.getDestinationDisplay().should.eventually.be.equal(true);
  });

  it("Should display the departure date field", async function() {
    await searchFormObject.departureDateFieldDisplay().should.eventually.equal(true);
  });

  it("Should display the return date field", async function() {
    await searchFormObject.returnDateFieldDisplay().should.eventually.be.equal(true);
  });

  it("Should display least price in ‘Cheapest’ sort option compared to ‘Best’ and ‘Quickest’ sort options", async function() {
    const cheapPrice = flightsPageObject.getCheapestPrice();
    const bestPrice = flightsPageObject.getBestPrice();
    const quickPrice = flightsPageObject.getQuickestPrice(); 
    await promise.all([cheapPrice,bestPrice,quickPrice]);
  });

  it("Should display least time in ‘Quickest’ sort option compared to ‘Cheapest’ and ‘Best’ sort options", async function() { 
    const cheapTime = await flightsPageObject.getCheapestTime();
    const bestTime = await flightsPageObject.getBestTime();
    const quickTime = await flightsPageObject.getQuickestTime();
    await promise.all([cheapTime, bestTime, quickTime]);
  });
});
