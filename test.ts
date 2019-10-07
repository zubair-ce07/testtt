import { browser, element, by, promise} from 'protractor';
import { HomePageObject } from './homePageObject';
import { FlightsPageObject } from './flightsPageObject';
import { CommonPageObject } from './commonPageObject';
import { async } from 'q';

var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
var should = chai.should();
let homePageObject: HomePageObject = new HomePageObject();
let flightsPageObject: FlightsPageObject = new FlightsPageObject();
let commonPageObject: CommonPageObject = new CommonPageObject();

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

  it("Should display the origin field", async function() {
    const departureDisplay = await commonPageObject.getDepartureDisplay();
    departureDisplay.should.equal(true);
  });

  it("Should display the destination field", async function() {
    const destinationDisplay = await  commonPageObject.getDestinationDisplay();
    destinationDisplay.should.equal(true);
  });

  it("Should display the departure date field", async function() {
    const departureDateDispalay = await commonPageObject.departureDateFieldDisplay();
    departureDateDispalay.should.equal(true);
  });

  it("Should display the return date field", async function() {
    const returnDateDisplay = await commonPageObject.returnDateFieldDisplay();
    returnDateDisplay.should.equal(true); 
  });

  it("Should display ‘Round-trip’ in trip type field", async function() {
    const roundTripType = await homePageObject.roundTripTypeField();
    roundTripType.should.equal(true); 
  });

  it("Switch to ‘One-way’ trip type mode", async function() {
    homePageObject.changeToOneWayTrip();
    const departureDateDispalay = await commonPageObject.departureDateFieldDisplay();
    departureDateDispalay.should.equal(true); 
  });
  
  it("Switch to ‘Multi-city’ trip type mode", async function() {
    homePageObject.changeToMulticityTrip();
    const multicityTripType = await homePageObject.multiCities();
    multicityTripType.should.equal(true);
  });

  it("Switch to ‘Round-trip’ trip type mode", async function() {
    await homePageObject.changeToRoundTrip();
    const roundTripType = await commonPageObject.returnDateFieldDisplay();
    roundTripType.should.equal(true);
  });

  it("Change number of ‘adults’ from travelers field to 9", async function() {
    await homePageObject.addAdultPassengers(10);
    const adultLimitMessage = await homePageObject.getAdultsLimitMessage();
    adultLimitMessage.should.equal("Searches cannot have more than 9 adults");
  });

  it("Should display ‘Paris (PAR)’ in origin field", async function() {
    await homePageObject.setDeparture();
    const departure = await homePageObject.getOriginValue()
    departure.should.equal("Paris (PAR)");
  });

  it("Should display ‘New York (NYC)’ in the destination field", async function() {
    await homePageObject.setDestination();
    const destination = await homePageObject.getDestinationValue();
    destination.should.equal("New York (NYC)");
  });

  it("Should display accurate date in departure field", async function() {
    homePageObject.fillDatesDeparture();
    expect(homePageObject.getDepartureDate()).to.eventually.equal(homePageObject.getTripDates(3));
  });

  it("Should display accurate date in return date field", function() {
    homePageObject.fillDatesReturn();
    expect(homePageObject.getReturnDate()).to.eventually.equal(homePageObject.getTripDates(6));
  });

  it("Should display all unchecked checkboxes in compare-to block", function() {
    homePageObject.uncheckAllCheckBox();
  });

  it("Should display ‘4 Travelers’ in the travelers field", async function() {
    homePageObject.decreaseAdultPassengers(6);
    const adultPassengers = await homePageObject.getAdultPassenger();
    adultPassengers.should.equal(4);
  });

  it("Should display ‘6 Travelers’ in the travelers field", function() {
    homePageObject.addChildPassengers(2);
    const childPassengers = homePageObject.getChildPassenger();
    childPassengers.should.equal(2);
  });

  it("Should display correct filled-in search form on results page", async function() {
    let searchUrl = await homePageObject.clickSearch();
    searchUrl.includes('sort=bestflight_a');
    });

  it("Should display the origin field", async function() {
    const departureDisplay = await commonPageObject.getDepartureDisplay();
    departureDisplay.should.equal(true);
  });

  it("Should display the destination field", async function() {
    const destinationDisplay = await  commonPageObject.getDestinationDisplay();
    destinationDisplay.should.equal(true);
  });

  it("Should display the departure date field", async function() {
    const departureDateDispalay = await commonPageObject.departureDateFieldDisplay();
    departureDateDispalay.should.equal(true); 
  });

  it("Should display the return date field", async function() {
    const returnDateDisplay = await commonPageObject.returnDateFieldDisplay();
    returnDateDisplay.should.equal(true);
  });

  it("Should display least price in ‘Cheapest’ sort option compared to ‘Best’ and ‘Quickest’ sort options", async function() {
    const cheapPrice =  flightsPageObject.getCheapestPrice();
    const bestPrice =   flightsPageObject.getBestPrice();
    const prices = await promise.all([cheapPrice,bestPrice]);

    expect(prices[0]).to.be.at.most(prices[1]);
  });

  it("Should display least time in ‘Quickest’ sort option compared to ‘Cheapest’ and ‘Best’ sort options", async function() { 
    const cheapTime = await flightsPageObject.getCheapestTime();
    const bestTime = await flightsPageObject.getBestTime();
    const quickTime = await flightsPageObject.getQuickestTime();
    const times = await promise.all([cheapTime, bestTime, quickTime]);

    expect(times[0]).to.be.at.most(times[1]);
  });
});
